import sys, os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))

import super_communicator

if __name__ == "__main__":
    print(sys.argv[-1])
    PID = sys.argv[-1]
    sys.argv.pop(len(sys.argv)-1)

    result = super_communicator.call_root_service(PID, "ChangeDirectory", sys.argv, app_name="CD Change Dir")
    print(f"[CD Change Dir] {result}")

