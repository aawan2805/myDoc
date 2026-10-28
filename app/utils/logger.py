import os
from datetime import datetime
from colorama import just_fix_windows_console

just_fix_windows_console()

VERDE = "\033[32m"
AZUL = "\033[34m"
NARANJA = "\033[38;5;208m"
ROJO = "\033[31m"
RESET = "\033[0m"


class AppLogger:
    def __init__(self, name: str):
        self.name = name

    def _print(self, color: str, level: str, message: str):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{color}{now} [{level}] {self.name}: {message}{RESET}")

    def ok(self, message: str):
        self._print(VERDE, "OK", message)

    def info(self, message: str):
        self._print(AZUL, "INFO", message)

    def warning(self, message: str):
        self._print(NARANJA, "WARNING", message)

    def error(self, message: str):
        self._print(ROJO, "ERROR", message)
