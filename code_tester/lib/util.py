import platform

class Util:
    def __init__(self):
        pass

    @staticmethod
    def get_os_name():
        os_name = platform.system().lower()
        if 'window' in os_name:
            return 'windows'
        if 'darwin' in os_name:
            return 'mac'
        if 'linux' in os_name:
            return 'linux'
        return None

