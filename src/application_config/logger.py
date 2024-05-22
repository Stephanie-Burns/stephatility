
import logging

from src.constants import LOGS_DIR


def configure_logger(
        name,
        log_to_console=True,
        log_to_file=False,
        file_path='logs/app.log',
        level=logging.INFO
):

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)-8s | %(module)s - %(funcName)s - %(message)s',
                      datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console logging setup
    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File logging setup
    if log_to_file:
        file_handler = logging.FileHandler(str(file_path))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


app_logger = configure_logger('StephAtilityLogger', file_path=LOGS_DIR, log_to_console=True, log_to_file=False)


if __name__ == '__main__':
    # Usage
    my_logger = configure_logger('MyAppLogger', log_to_console=True, log_to_file=True)
    my_logger.info('This log will go to both console and file.')

    # Switch to only file logging dynamically
    my_logger = configure_logger('MyAppLogger', log_to_console=False, log_to_file=True)
    my_logger.info('This log will go only to file.')
