import os
import time
import shutil
import warnings
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


folder_mapping = {
    ".pdf": "PDFs",
    ".txt": "TextFiles",
    ".png": "Images",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".doc": "Documents",
    ".docx": "Documents",
    ".xls": "Documents",
    ".xlsx": "Documents",
    ".ppt": "Documents",
    ".pptx": "Documents",
    ".zip": "Archives",
    ".rar": "Archives",
    ".gz": "Archives",
    ".tar": "Archives",
}

def move_file(file_path):
    filename = os.path.basename(file_path)
    file_ext = os.path.splitext(filename)[1].lower()
    if file_ext in folder_mapping:
        folder_name = folder_mapping[file_ext]
        destination_folder = os.path.join(os.path.dirname(file_path), folder_name)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        shutil.move(file_path, os.path.join(destination_folder, filename))
        print(f"Moved {filename} to {destination_folder}")

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            move_file(event.src_path)


class Watcher:
    def __init__(self, folder):
        self.folder = folder
        self.observer = Observer()

    def run(self):
        event_handler = MyHandler()
        try:
            self.observer.schedule(event_handler, self.folder, recursive=False)
        except NotImplementedError:
            warnings.warn("Failed to import read_directory_changes. Fall back to polling.")
            self.observer.schedule(event_handler, self.folder, recursive=False)
            self.observer.start()
        else:
            self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
            print("Watcher Stopped!")
        self.observer.join()

if __name__ == "__main__":
    folder_to_watch = r"C:\Users\kusha\Downloads"
    watcher = Watcher(folder_to_watch)
    watcher.run()
