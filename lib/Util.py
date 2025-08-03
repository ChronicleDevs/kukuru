import string
import os
import uuid
import random
class Util:
    @staticmethod
    def random_str_gen(length=12):
        chars = string.ascii_letters + string.digits  # abcABC123
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def MakeSession (root):
        pid = os.getpid()
        with open(root+"/"+str(pid)+".txt", "w") as t:
            t.write('')
        

    @staticmethod
    def is_valid_uuid(uuid_to_test, version=4):
        """
        Check if uuid_to_test is a valid UUID.
    
        Parameters
        ----------
        uuid_to_test : str
        version : {1, 2, 3, 4}
    
        Returns
        -------
        `True` if uuid_to_test is a valid UUID, otherwise `False`.
    
        Examples
        --------
        >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
        True
        >>> is_valid_uuid('c9bf9e58')
        False
        """
    
        try:
            uuid_obj = uuid.UUID(uuid_to_test, version=version)
        except ValueError:
            return False
        return str(uuid_obj) == uuid_to_test