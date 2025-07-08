import os


def clear_console(): return os.system('cls' if os.name == 'nt' else 'clear')