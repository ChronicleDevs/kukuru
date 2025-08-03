import sys, os, json
from colorama import Fore, Style, init
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))

import super_communicator

# Wajib untuk Windows atau agar langsung jalan
init(autoreset=True)
if __name__ == "__main__":
    print(sys.argv[-1])
    PID = sys.argv[-1]
    sys.argv.pop(len(sys.argv)-1)
    sys.argv.pop(len(sys.argv)-1)
    result = super_communicator.call_root_service(PID, "ListDirectory", sys.argv, app_name="LS Listdir")
    
    try:
        result = json.loads(result["message"])
        ctr = 1
        for name, info in result.items():
            color = ""
        
            if info.get("is_symlink"):
                color = Fore.MAGENTA
            elif info.get("is_hidden"):
                color = Fore.YELLOW
            elif info.get("type") == "directory":
                color = Fore.BLUE
            elif info.get("type") == "file":
                color = Fore.GREEN

            suffix = ""
            if info.get("type") == "directory" and info.get("is_empty") == 1:
                suffix = " [empty]"

            if ctr < 3:
                print(f"{color}{name}{suffix}{Style.RESET_ALL}", end='\t')
                ctr+=1

            else: 
                print(f"{color}{name}{suffix}{Style.RESET_ALL}")
                ctr = 1

        print("")
    except json.JSONDecodeError:
        print(result["message"])


