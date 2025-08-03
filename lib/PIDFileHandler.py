import os, path, sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class PIDFileHandler(FileSystemEventHandler):
    def __init__(self, manager):
        # Register manager
        self.manager = manager
        print("Watch activated")

    def on_deleted(self, event):
        filename = os.path.basename(event.src_path)
        print("Watch detected file remove")
        if not event.is_directory:
            with self.manager._lock:
                if str(filename).replace('.txt','') in self.manager._session:
                    del self.manager._session[self.manager._session.index(str(filename).replace('.txt',''))]
                    #print(str(filename).replace('.txt', ''))
                    #print(self.manager.PID)
                    #print(str(filename).replace('.txt', '') == str(self.manager.PID))
                    if str(filename).replace('.txt','') == str(self.manager.PID):
                        exit(2)

    def on_created(self, event):
        filename = os.path.basename(event.src_path)
        print("Watch detected file addition")
        if not event.is_directory:
            with self.manager._lock:
                if not filename in self.manager._session:
                    self.manager._session.append(filename)
