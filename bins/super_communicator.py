import redis
import json

r = redis.Redis()
import random
import socket

def call_root_service(pid, action, argv, app_name="UnknownApp"):
    reg_key = f"registry:{pid}"
    if not r.exists(reg_key):
        return {"status": "ERROR", "message": f"No registry for PID {pid}"}

    entries = r.hgetall(reg_key)
    choices = []

    for k, v in entries.items():
        item = json.loads(v.decode())
        if not item.get("in_use"):
            choices.append(item["path"])

    if not choices:
        return {"status": "ERROR", "message": "All sockets in use"}

    chosen_path = random.choice(choices)
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        client.connect(chosen_path)
        req = {
            "action": action,
            "argv": argv,
            "app": app_name
        }
        client.send(json.dumps(req).encode())
        resp = client.recv(4096)
        return json.loads(resp.decode())
    except Exception as e:
        import traceback
        return {"status": "ERROR", "message": "!ERR "+str(e)}
    finally:
        client.close()


