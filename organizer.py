import json
import shutil
import time
import os
from pathlib import Path

class FileOrganizer:
    def __init__(self, config_path):
        self.config_path = Path(config_path).resolve()
        self.rules = self.load_rules()

    def load_rules(self):
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def get_destination_folder(self, file_path):
        suffix = file_path.suffix.lower()
        for rule in self.rules['rules']:
            if suffix in rule['extensions']:
                return rule['target_dir']
        return self.rules.get('default_folder', 'Others')

    def process_file(self, file_path):
        file_path = Path(file_path)
        
        # 1. Skip if it's a directory or temporary browser file
        if file_path.is_dir() or file_path.suffix in ['.crdownload', '.tmp', '.part']:
            return

        # 2. WAIT FOR FILE TO BE READY (The "Perfect" part)
        # This loop waits until the browser releases the file
        retries = 5
        while retries > 0:
            try:
                # Try to rename the file to itself; if it fails, the file is still "in use"
                with open(file_path, 'a'):
                    break 
            except IOError:
                time.sleep(2)
                retries -= 1
        
        if retries == 0:
            return # Skip if file is stuck

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
        except Exception as e:
            print(f"Error moving {file_path.name}: {e}")