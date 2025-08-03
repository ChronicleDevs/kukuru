import sys, os
sys.path.append(os.path.abspath(os.path.join(__file__, "..", "..", "..", "..")))

import super_communicator

if __name__ == "__main__":
    print(sys.argv[-1])
    result = super_communicator.call_root_service(sys.argv[-1], "Ping", "cache/", app_name="CacheRemover")
    print(f"[CacheRemover] {result}")

