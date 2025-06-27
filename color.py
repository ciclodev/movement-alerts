import logging

from colorama import Style


class ColorFormatter(logging.Formatter):
    def format(self, record):
        color = getattr(record, 'color', '')
        msg = super().format(record)
        return f"{color}{msg}{Style.RESET_ALL}"
