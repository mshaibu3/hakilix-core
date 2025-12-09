import logging
import colorlog
import sys
def setup_logger(name):
    handler = colorlog.StreamHandler(sys.stdout)
    handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s'))
    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger