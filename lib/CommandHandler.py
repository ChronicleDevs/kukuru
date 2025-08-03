import os
import subprocess
import random
import json
from pathlib import Path
import sys

class CommandHandler:
    """
    Command Handler by RYU

    /bins/sys - for essentials system programs
    /bins/usr - for users system programs

    Example of program tree
    - System/User Prog.
    /bins/(usr or sys)/(name)/-- program.py
                     |_ info.json
                     |_ libs/ -- (another libs).py
                     |_ conf/ -- (conf).conf

    """ 

    def __init__(self, root, PID, UtilInstance):
        # Define constants
        self.__PATH = str(root)+"/bins"
        self.__SYSP = self.__PATH+"/sys"
        self.__USRP = self.__PATH+"/usr"
        self.__PID = PID
        self.Util = UtilInstance
        self.__ROOT = str(root)
        # Call essential funs
        print("[!] Loading essentials CMD..")
        self.__Scan()
        print("[V] Successfully loaded.")

    def exc(self, tx, args):
        if not tx in self.__SysBIN.keys():
            return (False, 'Command not found')
        else:
            try:

                cmd = self.__SysBIN[tx]["cmd"][tx]["bin"].replace("(app_root)", self.__SysBIN[tx]['path'])
                return self.__run_bin_py(self.__SysBIN[tx]['path_venv'],  cmd, args)
                

            except KeyError:
                return (False, 'Command Not Found or Invalid Configuration.')





    def __Setupvenv(self, target_dir):
        target = Path(target_dir).resolve()
        venv_dir = target / ".venv"
    
        # Step 1: Buat venv
        print(f"[+] Membuat virtual environment di {venv_dir}")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)
        except subprocess.CalledProcessError as e:
            print("[!] Failed to setup virtual env!")
        # Step 2: Install dependensi
        pip_path = venv_dir / "bin" / "pip"
        req_path = target / "requirements.txt"
        if req_path.exists():
            print(f"[+] Menginstal requirements dari {req_path}")
            subprocess.run([str(pip_path), "install", "-r", str(req_path)], check=True)
        else:
            print("[!] requirements.txt tidak ditemukan, lanjut tanpa install.")

        return venv_dir

    def __run_bin_py(self, venv_dir, bin_path, args):
        a = args.copy()
        a.append(self.__ROOT)
        a.append(str(self.__PID))
        python_path = venv_dir+"/bin/python"
        print(f"[+] Menjalankan {bin_path} dengan python dari venv...")
        try: 
            subprocess.run([str(python_path), str(bin_path)] + a, check=True)
            return (True, '')
        except (subprocess.CalledProcessError, subprocess.SubprocessError) as e:
            print("[!] Error occured when running the application. Stopping app..")
            return (False, "")
    def __Scan(self):
        x_sys = os.listdir(self.__SYSP)
        x_usr = os.listdir(self.__USRP)
        _x = self.__TreeCheck(x_sys, v=True)

        self.__SysBIN = {}
    
        for key, val in _x.items():
            path = val["path"]
            if not os.path.exists(path + "/.venv"):
                self.__Setupvenv(Path(path))
            val = val.copy()  # supaya gak ubah yang lama
            val["path_venv"] = os.path.join(path, ".venv")
            _cmds = val["cmd"]
            for i in _cmds.keys():
                self.__SysBIN[i] = val
            #self.__SysBIN[key] = val

        

    





    def __TreeCheck(self, dirv, s=False, v=False):
        def convert(sd, sign, rep):
            return sd.replace('[[['+sign+']]]', rep)

        if not s:
            svalid = {}
            signature = self.Util.random_str_gen(64)
            sys_bd = self.__SYSP + "/[[["+signature+"]]]"
            sysbp = sys_bd+'/bin'
            sysnfo = sys_bd+'/info.json'

            for x in dirv:
                if v:
                    print("\n\nRegistering app with path: ", self.__SYSP+"/"+x)
                if os.path.exists(self.__SYSP+"/"+x):
                    if os.path.exists(convert(sysbp, signature, x)) and os.path.exists(convert(sysnfo, signature, x)):
                        if v: print("!- Registering binary with following path: "+convert(sysbp, signature, x))
                        try:
                            with open(convert(sysnfo, signature, x)) as nfo:
                                yd = json.load(nfo)
                                if v: print("!-- ", yd, "\n\n")
                                if self.Util.is_valid_uuid(yd["uuid"]):
                                    yd["path"] = self.__SYSP+"/"+x
                                    for i in yd["cmd"].keys():
                                        svalid[i] = yd
                                else:
                                    print("Invalid UUID")
                                    continue
                        except FileNotFoundError:
                            print("Config File Doesn't exists")
                            continue
                        except json.JSONDecodeError:
                            print("Invalid Config File")
                            continue
            return svalid


