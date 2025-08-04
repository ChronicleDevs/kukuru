import sys, os, json
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))
from pathlib import Path
import super_communicator


class YookaPackageManager:
    def __init__(self, PID):
        self.name = "Yooka Package Manager"
        self.PID = PID
        self.root = json.loads(super_communicator.call_root_service(self.PID, "GetSystemInfo", '', app_name="YO Yooka Package Manager")["message"])['root']

    # Fungsi virtualize_path seperti yang dijelaskan
    def virtualize_path(self, p: str, virtual_root: str = "/") -> str:
        p = Path(p).resolve()
        real_root = Path(self.root).resolve()
        try:
            relative = p.relative_to(self.root)
            return str(Path(virtual_root) / relative)
        except ValueError:
            # Path is outside the real_root
            return str(p)

    def print_package_tree(self, data: dict):
        print("System Packages:")
        sys_data = data.get("sys", {})
        if not sys_data:
            print("  (None)")
        for uuid, meta in sys_data.items():
            name = meta.get("name", "(Unnamed)")
            print(f"├── {uuid}")
            print(f"│   ├── Name: {name}")
            if "author" in meta:
                print(f"│   ├── Author: {meta['author']}")
            if "version" in meta:
                print(f"│   ├── Version: {meta['version']}")
            if "description" in meta:
                print(f"│   ├── Description: {meta['description']}")
            if "path" in meta:
                print(f"│   ├── Path: {self.virtualize_path(meta['path'])}")
            if "path_venv" in meta:
                print(f"│   ├── VirtualEnv: {self.virtualize_path(meta['path_venv'])}")
            cmds = meta.get("cmd", {})
            print("│   └── Commands:")
            for cmd, info in cmds.items():
                about = f" [{info['about']}]" if "about" in info else ""
                print(f"│       ├── {cmd} → {info['bin']}{about}")
            print("│")

        print("User Packages:")
        usr_data = data.get("usr", {})
        if not usr_data:
            print("  (Empty)")
        # You can extend for usr packages similarly




    def __sendRequest(self, request):
        return super_communicator.call_root_service(self.PID, "PackageManagerUtilities", json.dumps(request), app_name="YO Yooka Package Manager")
    def exe(self, ags, package, opts):
        request = {}
        if ags == "resetvenv" or ags == "rv":
            package = package[0]
            if ':' not in package:
                print("[!] Please type valid package name, [usr or sys]:[packagename], example: sys:yooka, usr:calculator")
                return 0
            if package.split(':')[0] != "sys" and package.split(':')[0] != 'usr':
                print("[!] Please type valid package name, [usr or sys]:[packagename], example: sys:yooka, usr:calculator")
                return 0
            request = {"request": 'reset-venv', 'package': package}
            x = self.__sendRequest(request)
            print(x)



        elif ags == "allinfo" or ags == "ai":
            request = {'request': 'get-all-pkginfo'}
            x = self.__sendRequest(request)
            # print(x['message'])
            self.print_package_tree(json.loads(x['message'].replace("'", '"')))
        elif ags == "help" or ags == "h":
            print(self.help())

            

    def help(self):
        return """

        Yooka Package Manager — Help

        ~ is a basic package manager shell.
        Usage: yo [COMMAND] [ARGS] (options)

        Here are basic commands:
        - i / install: Install package(s)
        - u / uninstall: Unibstall package(s)
        - r / reinstall: Reinstall package(s)
        - re / reset: Reset config of a package
        - rv / resetvenv: Resetup virtual env of a package.
        - if / info: Show information about a package
        - ai / allinfo: Show all installed package(s)' information.
        - v / version: Show current version of Yo Package Manager

        Enjoy yooka-ing XD!!
        Credit: Yokadexyl


        """

    def parse(self, agv):
        """
        yo [command] [package] (options)

        """

        cmd = ''
        ag = []
        if len(agv) == 1:
            cmd = agv[0]
            cmd.strip()
        elif len(agv) > 1:
            cmd = agv[0]
            agv.pop(0)
            ag = agv.copy()

        options = []
        for i in ag:
            if i.strip().startswith('-'):
                options.append(i)
                del ag[ag.index(i)]
        
        return cmd, ag, options


if __name__ == "__main__":
    sys.argv.pop(0)
    PID = sys.argv[-1]
    yooka = YookaPackageManager(PID)

    root = sys.argv[-2]
    sys.argv.pop(len(sys.argv)-1)
    sys.argv.pop(len(sys.argv)-1)
    print(sys.argv)
    if len(sys.argv) == 0:
        print("Yooka Package Manager v1.0 --is a basic package manager by Yokadexyl.\nIt is written in Python3.\n\nPlease run 'yo help' to show help\n\nHope you enjoy yooka-ing XD\n\n")
    cmd, argvs, opts = yooka.parse(sys.argv)
    yooka.exe(cmd, argvs, opts)
    
