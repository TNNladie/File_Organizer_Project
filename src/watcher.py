import time
import logging
import os
import json
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Ensure we can import sibling modules if needed, but we try to keep this standalone-capable
# for the specific user request of "only changes in watcher.py"
try:
    from src.organizer import FileOrganizer
    HAS_ORGANIZER = True
except ImportError:
    # Try adjusting path if run directly
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    try:
        from src.organizer import FileOrganizer
        HAS_ORGANIZER = True
    except ImportError:
        HAS_ORGANIZER = False

class WatcherHandler(FileSystemEventHandler):
    def __init__(self, organizer=None):
        self.organizer = organizer

    def on_created(self, event):
        path_type = "DIRECTORY" if event.is_directory else "FILE"
        message = f"!!! NEW {path_type} DETECTED: {event.src_path} !!!"
        print(message)
        logging.info(message)
        
        # Short delay to safeguard against incomplete writes
        time.sleep(1)
        
        if not event.is_directory and self.organizer:
            try:
                self.organizer.organize_file(event.src_path)
                print(f"-> Organized: {event.src_path}")
            except Exception as e:
                print(f"-> Error organizing: {e}")
        elif event.is_directory:
             print(f"-> Directory detected, skipping organization logic for folder.")
        elif not self.organizer:
            print("-> No organizer available, just watching.")

class Watcher:
    def __init__(self, directory, organizer=None):
        self.directory = directory
        self.organizer = organizer
        self.observer = Observer()
        self.handler = WatcherHandler(organizer)

    def start(self):
        print(f"--- Watcher Started on: {self.directory} ---")
        print("Waiting for new files and directories...")
        
        print("Performing initial scan...")
        self.scan_existing()
        print("Initial scan done. Now monitoring...")

        self.observer.schedule(self.handler, self.directory, recursive=False)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        print("Stopping watcher...")
        self.observer.stop()
        self.observer.join()

    def scan_existing(self):
        if not os.path.exists(self.directory):
            print(f"Directory not found: {self.directory}")
            return
            
        items = os.listdir(self.directory)
        for item in items:
            full_path = os.path.join(self.directory, item)
            item_type = "Directory" if os.path.isdir(full_path) else "File"
            print(f"[Existing {item_type} Found]: {full_path}")
            
            if os.path.isfile(full_path) and self.organizer:
                self.organizer.organize_file(full_path)

if __name__ == "__main__":
    # Standalone execution logic
    
    # Load config to find path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, 'config.json')
    
    target_dir = None
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                target_dir = config.get('source_directory')
        except Exception as e:
            print(f"Error loading config: {e}")

    # Fallback or validate
    if not target_dir or target_dir == "{gelecek}":
        print("Config 'source_directory' is invalid using current directory for testing.")
        target_dir = os.getcwd() 
    
    # Setup simple logger to console
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

    # Try init organizer
    organizer = None
    if HAS_ORGANIZER and 'config' in locals():
         organizer = FileOrganizer(config)

    w = Watcher(target_dir, organizer)
    w.start()
