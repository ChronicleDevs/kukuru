from colorama import Fore, Style
from pathlib import Path
import os
import string
import random
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import signal
import atexit
import json
import uuid
import socket
import subprocess
import sys
import traceback
import shutil
import redis

from lib.PIDFileHandler import PIDFileHandler
from lib.PySHAPI.pyshapi import PySHAPI
from lib.CommandHandler import CommandHandler
from lib.Util import Util



class PySH:
    def __init__(self):
        # define constants
        self.__VERSION = "1.0p"
        self.__NAME = "Python non-integrated Shell"
        self.__ROOT = Path(__file__).parent
        self.__SESSION_PATH = str(self.__ROOT)+"/sessions"
        self.__REGISTRY_FILE = str(self.__ROOT)+"/nsc/registry.json"
        self.PID = os.getpid()
        
        self.__SOCKET = str(self.__ROOT)+"/nsc"
        self.__NUM_SOCK = 256

        
        self.__redis = redis.Redis()

        # Rewrite signals
        signal.signal(signal.SIGINT, self.__exit)
        signal.signal(signal.SIGTERM, self.__exit)
    
    

        try:
            # Run essentials fn's
            Util.MakeSession(self.__SESSION_PATH)
            if os.path.exists(self.__SOCKET+str(self.PID)):
                shutil.rmtree(self.__SOCKET+str(self.PID))

            self.__redis.delete("registry:{self.PID}")


    

            # define required/essentials vars
            self.__observer = Observer()
            self._session = self.__detectSession()
            self._lock = threading.Lock()

            self.__watchSession()

            for i in range(self.__NUM_SOCK):
                threading.Thread(target=self.__socket_server, args=(i,), daemon=True).start()
            
        

            self.__cmd = CommandHandler(self.__ROOT, self.PID, Util)
            self.startShell()
            
        except Exception as e:
            print("There is an error, exiting.. \n\n")
            print(traceback.format_exc())
            os.remove(self.__SESSION_PATH+"/"+str(self.PID)+".txt")

    def __PANIC(self):
        print('[' + Fore.RED + " PANIC! " + Style.RESET_ALL + "] There is a fatal error.")


    """
    ShellAPI, the way that allow app to communicate with the server/daemon (the root/shell)
    it uses Socket mechanic

    """

    def __update_registry(self, sock_name, status, path):
        entry = {"in_use": status, "path": path}
        self.__redis.hset(f"registry:{self.PID}", sock_name, json.dumps(entry))


    def __handle_client(self, conn, index):
        sock_name = f"sock{index}"
        sock_path = self.__SOCKET+"/"+str(self.PID)+"/"+sock_name + ".sock"
        self.__update_registry(sock_name, True, sock_path)
        try:
            data = conn.recv(4096)
            request = json.loads(data.decode())
            print(f"[shell:{self.PID}] Request from {request['app']} -> {request['action']} {request['argv']}")

            # Basic authorization check
            ps = PySHAPI(self.__ROOT)
            response = ps.Check(request)
            #if request['action'] == "Ping":
            #    response = {"status": "OK", "message": "AHOY!!"}
            #elif request['action'] == "RemoveAll" and request['target'].startswith("cache/"):
            #    os.system(f"rm -rf {request['target']}")
            #    response = {"status": "OK", "message": f"Deleted {request['target']}"}
            #else:
            #    response = {"status": "DENIED", "message": "Unauthorized or invalid action"}

            conn.send(json.dumps(response).encode())
        except Exception as e:
            print(traceback.format_exc())
            conn.send(json.dumps({"status": "ERROR", "message": str(e)}).encode())
        finally:
            self.__update_registry(sock_name, False, sock_path)
        conn.close()

    def __socket_server(self,index):
        sock_name = f"sock{index}"

        os.makedirs(self.__SOCKET+"/"+str(self.PID),exist_ok=True)

        sock_path = self.__SOCKET+"/"+str(self.PID)+"/"+sock_name + ".sock"

        if os.path.exists(sock_path):
            os.remove(sock_path)
        


        server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server.bind(sock_path)
        server.listen(5)
        self.__update_registry(sock_name, False, sock_path)

        while True:
            conn, _ = server.accept()
            threading.Thread(target=self.__handle_client, args=(conn, index), daemon=True).start()

    """
    Session handling System

    all sessions are stored in (root)/sessions
    every sessions have its instance, so if a session file removed (by force), it'll destroy a shell instance related to the session file


    """

    def __detectSession (self):
        # Check if the directory exists
        if not os.path.exists(self.__SESSION_PATH):
            self.__PANIC()

        _d = os.listdir(self.__SESSION_PATH)
        d = []
        for i in _d:
            d.append(i.replace('.txt', ''))
        return d

    def __watchSession(self):
        handler = PIDFileHandler(self)
        self.__observer.schedule(handler, self.__SESSION_PATH, recursive=False)
        self.__observer.start()


    """
    Main/Core of the program

    """
    def startShell(self):
        print("PySH v1. PROTOTYPE/UNDER DEVELOPMENT\nPlease type 'help' to show essential commands\nHave Fun XD\n\n")
        while True:
            x = input("[PySH: "+str(len(self._session))+" session(s) active]")
            cmd = ""
            args = []
            if " " in x:
                cmd = x.split(' ')[0]
                args = x.split(' ')
                args.pop(0)
            else: cmd = x
            print("-- Processing command: ", cmd, " with args: ", args)
            res = self.__cmd.exc(cmd, args)
            if not res[0]:
                print("[ERROR] ", res[1])
            

    
    def __exit(self, signum, frame):
        print("Exiting ..")
        os.remove(self.__SESSION_PATH+"/"+str(self.PID)+".txt")
        shutil.rmtree(self.__SOCKET+"/"+str(self.PID), ignore_errors=True)
        self.__redis.delete("registry:{self.PID}")
        exit(2)


PySH()
