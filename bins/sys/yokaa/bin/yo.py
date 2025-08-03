import sys, os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))

import super_communicator

if __name__ == "__main__":
    sys.argv.pop(0)
    PID = sys.argv[-1]
    root = sys.argv[-2]
    sys.argv.pop(len(sys.argv)-1)
    sys.argv.pop(len(sys.argv)-1)
    print(sys.argv)
    if len(sys.argv) == 0:
        print("Yooka Package Manager v1.0 --is a basic package manager by Yokadexyl.\nIt is written in Python3.\n\nPlease run 'yo help' to show help\n\nHope you enjoy yooka-ing XD\n\n")
        
    