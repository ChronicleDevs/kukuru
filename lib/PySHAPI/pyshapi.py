from pathlib import Path
import os
import json

class FSRead:
    @staticmethod
    def cd_v(target, wl):
        if os.path.exists(str(target)):
            if wl == target or wl in target.parents:
                os.chdir(Path(target).resolve())
                return {"status": "OK", "message": ""}
            else:
                return {"status": "ERROR", "message": "You don't have any permission to access this directory"}
        else:
                return {"status": "ERROR", "message": "Directory not found."}

    @staticmethod
    def ls_v(target, wl):
        print(target)
        if os.path.exists(str(target)):
            if wl == target or wl in target.parents:
                target_path = Path(target).resolve()
                if not target_path.is_dir():
                    return {"status": "ERROR", "message": "Cannot list, not a directory"}

                result = {}
                for entry in target_path.iterdir():
                    info = {
                        "absolute": str(entry.resolve()),
                        "type": "directory" if entry.is_dir() else "file",
                        "is_hidden": int(entry.name.startswith(".")),
                        "is_symlink": int(entry.is_symlink()),
                    }
                    if entry.is_dir():
                        try:
                            info["is_empty"] = int(not any(entry.iterdir()))
                        except PermissionError:
                            info["is_empty"] = -1  # atau bisa raise
                    result[entry.name] = info

                return {"status": "OK", "message": json.dumps(result)}
            else:
                return {"status": "ERROR", "message": "You don't have any permission to access this directory"}
        else:
            return {"status": "ERROR", "message": "Directory not found."}


class PySHAPI:
    def __init__(self,root):
        self.__root = root

    def Check(self,__request):
        # Parse user args
        args = __request["argv"]
        args.pop(0)
        options = []
        for i in args:
            if i.startswith('-'):
                options.append(i)
                del args[args.index(i)]

        FSAPI = ['ChangeDirectory', 'ListDirectory', 'Remove', 'Create']
                
        def resolve_user_path(user_input: str, root: Path) -> Path:
            user_path = Path(user_input)

            if Path(user_input).resolve() == root.resolve():
                return root.resolve()
            if user_input.startswith("/"):
                # Treat sebagai relative ke root
                user_path = root.joinpath(user_path.relative_to("/"))
            else:
                #    Path relatif biasa dari cwd
                user_path = Path(user_input)

            return user_path.resolve()
        # def resolve_user_path(user_input: str, root: Path) -> Path:
        #     user_path = Path(user_input)



        #     if user_path.is_absolute():
        #         try:
        #         # Hilangkan leading "/" agar relatif terhadap virtual root
        #             user_path = user_path.relative_to("/")
        #         except ValueError:
        #             raise PermissionError(f"Path {user_input} is outside virtual root")

        #     combined = (root / user_path).resolve()

        #     # Pastikan hasil akhir tetap dalam root
        #     if not combined.is_relative_to(root):
        #         raise PermissionError(f"Access outside virtual root is denied: {combined}")

        #     return combined

        __root = self.__root



        if __request['action'] in FSAPI:

            # Define prohibited CD.
            __wl = Path(str(__root)+"/home")

            if __request['action'] == 'ChangeDirectory':
                args = ['/home'] if len(args) == 0 else args
                __target = resolve_user_path(args[0], __root)
            
                return FSRead.cd_v(__target, __wl)

            elif __request['action'] == 'ListDirectory':
                args = ['.'] if len(args) == 0 else args
                __target = resolve_user_path(args[0], __root)


                return FSRead.ls_v(__target, __wl)
            elif __request['action'] == 'PackageManagerUtilities':
                print(args)
            