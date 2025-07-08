import logging
import sys
from colorama import init

from color import ColorFormatter

init(autoreset=True)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.propagate = False          # ¡corta la subida al root!

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(ColorFormatter(
    "%(asctime)s - [%(levelname)s] %(message)s"))
logger.addHandler(handler)
