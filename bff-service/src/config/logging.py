import logging
import sys


def set_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
        force=True,
    )
