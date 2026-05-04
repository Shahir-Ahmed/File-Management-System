import json
import shutil
import time
from pathlib import Path

class FileOrganizer:
    def __init__(self, config_path, watch_folder=None):
        self.config_path = Path(config_path).resolve()
        self.watch_folder = Path(watch_folder).resolve() if watch_folder else None
        self.rules = self.load_rules()
        self.managed_roots = self._build_managed_roots()

    def load_rules(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def _build_managed_roots(self):
        roots = set()
        for rule in self.rules.get('rules', []):
            target = rule.get('target_dir', '').strip('/\\')
            if target:
                roots.add(target.split('/')[0].split('\\')[0])

        default_folder = self.rules.get('default_folder', '').strip('/\\')
        if default_folder:
            roots.add(default_folder.split('/')[0].split('\\')[0])

        return roots

    def get_destination_folder(self, file_path):
        suffix = file_path.suffix.lower()
        for rule in self.rules['rules']:
            if suffix in rule['extensions']:
                return rule['target_dir']
        return self.rules.get('default_folder', 'Others')

    def is_eligible_file(self, file_path):
        if file_path.is_dir() or file_path.suffix.lower() in ['.crdownload', '.tmp', '.part']:
            return False

        if self.watch_folder:
            try:
                rel_path = file_path.resolve().relative_to(self.watch_folder)
            except ValueError:
                return False

            # Only organize new files dropped directly in Downloads root.
            if len(rel_path.parts) != 1:
                return False

            if rel_path.parts and rel_path.parts[0] in self.managed_roots:
                return False

        return True

    def wait_for_file_ready(self, file_path):
        previous_size = -1
        stable_checks = 0
        attempts = 12  # around 24 seconds with 2s pause

        for _ in range(attempts):
            if not file_path.exists():
                time.sleep(1)
                continue

            try:
                current_size = file_path.stat().st_size
                with open(file_path, 'rb'):
                    pass
            except (PermissionError, OSError):
                time.sleep(2)
                continue

            if current_size == previous_size:
                stable_checks += 1
                if stable_checks >= 2:
                    return True
            else:
                stable_checks = 0
                previous_size = current_size

            time.sleep(2)

        return False

    def process_file(self, file_path):
        file_path = Path(file_path).resolve()
        
        # 1. Skip ineligible files
        if not self.is_eligible_file(file_path):
            return

        # 2. Wait until download is complete and the file is stable
        if not self.wait_for_file_ready(file_path):
            print(f"Skipped (not ready): {file_path.name}")
            return

        # 3. Determine Destination
        dest_subfolder = self.get_destination_folder(file_path)
        dest_dir = file_path.parent / dest_subfolder
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # 4. Handle Duplicate Names
        target_path = dest_dir / file_path.name
        counter = 1
        while target_path.exists():
            # If "image.jpg" exists, try "image_1.jpg", then "image_2.jpg"
            target_path = dest_dir / f"{file_path.stem}_{counter}{file_path.suffix}"
            counter += 1

        # 5. Move the file
        try:
            shutil.move(str(file_path), str(target_path))
            print(f"Organized: {file_path.name} -> {dest_subfolder}")
        except FileNotFoundError:
            print(f"Skipped (missing): {file_path.name}")
        except Exception as e:
            print(f"Error moving {file_path.name}: {e}")