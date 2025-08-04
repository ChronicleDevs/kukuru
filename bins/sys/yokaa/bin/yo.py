import sys, os, json
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))

import super_communicator


class YookaPackageManager:
    def __init__(self):
        self.name = "Yooka Package Manager"

    def parse(self, ags, package):
        if ags == "resetvenv":
            request = {"act": 'resetvenv', 'package': package}
            result = super_communicator.call_root_service(PID, "PackageManagerUtilies", json.dumps(reques5), app_name="YO Yooka Package Manager")


    def help(self):
        return """"

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
        - v / version: Show current version of Yo Package Manager

        Enjoy yooka-ing XD!!
        Credit: Yokadexyl


        """

if __name__ == "__main__":
    sys.argv.pop(0)
    PID = sys.argv[-1]
    root = sys.argv[-2]
    sys.argv.pop(len(sys.argv)-1)
    sys.argv.pop(len(sys.argv)-1)
    print(sys.argv)
    if len(sys.argv) == 0:
        print("Yooka Package Manager v1.0 --is a basic package manager by Yokadexyl.\nIt is written in Python3.\n\nPlease run 'yo help' to show help\n\nHope you enjoy yooka-ing XD\n\n")
        
    
