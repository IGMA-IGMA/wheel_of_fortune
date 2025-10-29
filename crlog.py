import logging

def create_logger():

    logger = logging.getLogger("game")
    logger.setLevel(logging.CRITICAL)

    logfile = logging.FileHandler("game.log")

    fmt = '[%(asctime)s] - %(levelname)s - %(message)'