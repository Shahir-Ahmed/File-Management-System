import time
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from organizer import FileOrganizer
import os
import logging

logging.basicConfig(
    filename='file_organizer.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Replace your print() calls with:
# logging.info(f"Moved {file_path.name}")
# --- CONFIGURATION ---
# Path.home() / "Downloads" points to your system's default Download folder
WATCH_FOLDER = str(Path.home() / "Downloads") 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "rules.json")

class DownloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.organizer = FileOrganizer(CONFIG_FILE, WATCH_FOLDER)

    def on_created(self, event):
        # Triggered when a new file is created
        if not event.is_directory:
            self.organizer.process_file(event.src_path)

    def on_moved(self, event):
        # Browsers often 'move' a .crdownload file to a .pdf file when finished
        if not event.is_directory:
            self.organizer.process_file(event.dest_path)

if __name__ == "__main__":
    # Ensure the folder exists
    if not Path(WATCH_FOLDER).exists():
        print(f"Error: The folder {WATCH_FOLDER} does not exist.")
        sys.exit(1)

    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    
    print(f"!!! Smart File System Active !!!")
    print(f"Monitoring: {WATCH_FOLDER}")
    print("Press Ctrl+C to stop.")
    
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping Smart File System...")
    observer.join()