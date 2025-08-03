import sys, os, json
from colorama import Fore, Style, init
init(autoreset=True)


from pathlib import Path



def virtual_path(root, real: str) -> str:
    real_path = Path(real).resolve()
    try:
        relative = real_path.relative_to(root)
        return "/" + str(relative)
    except ValueError:
        # Path di luar scope root → jangan izinkan
        print("Couldn't get the path, out of bound.")

if __name__ == "__main__":
    root = Path(sys.argv[-2]).resolve()
    print(virtual_path(root, '.'))



