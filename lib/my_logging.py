# Standard libs
import datetime
import logging
import os

# Third-party
import numpy as np

LOGGERNAME = "main"


def create_logger(log_file):
    """Creates a logger instance with two handlers, one for the console
    (levels DEBUG and worse) and one for an output log (levels INFO and worse).

    :param log_file: Name of output log file. Will be created if it does not
        exist, and is written to in append mode.
    :type log_file: string
    :return: logger
    :rtype: logging.RootLogger
    """
    logger = logging.getLogger(LOGGERNAME)
    # Avoid creating new handlers
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s | [%(levelname)s]:" "%(name)s :%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        formatter_1 = logging.Formatter(
            "%(asctime)s | [%(levelname)s]:" "%(filename)s:%(funcName)20s :%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        logger.setLevel(logging.DEBUG)
        # File handler
        fh = logging.FileHandler(filename=log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        # Console stream handler
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        sh.setFormatter(formatter)
        # Add handlers to logger object
        logger.addHandler(fh)
        logger.addHandler(sh)

    return logger


def start_logging(log_dir, info="", dt_frmt="%Y_%m_%d_%H_%M_%S", keep_num=100):
    """Starts a new logger and stores in log_dir, also deletes old logs

    :param log_dir: Dir to store log files, will be created if it doesnt exist
    :type log_dir: str
    :param info: Information to store in log file name, defaults to ''
    :type info: str, optional
    :param dt_frmt: Format to store the timestamp in (goes in the filename)
    :type dt_frmt: str, optional
    :param keep_num: number of latest files to keep, defaults to 100
    :type keep_num: int, optional
    :return: logger
    :rtype: logging.RootLogger
    """
    # Create a log_dir if it doesn't exist
    if os.path.isdir(log_dir) is not True:
        os.mkdir(log_dir)
    logger = create_logger(
        os.path.join(
            log_dir, datetime.datetime.now().strftime(dt_frmt) + "-" + info + ".log"
        )
    )
    delete_old_logs(log_dir, dt_frmt, keep_num)

    return logger


def delete_old_logs(log_dir, dt_frmt, keep_num):
    """Deletes old log files. Expects the files to start with timestamp.

    :param log_dir: Directory to search for the log files
    :type log_dir: str
    :param logger: Logger object
    :type logger: logging.RootLogger
    :param dt_frmt: Format of the timestamp in the filenames
    :type dt_frmt: str
    :param keep_num: number of latest files to keep, defaults to 100
    :type keep_num: int
    """
    logger = logging.getLogger(LOGGERNAME)
    filenames = [
        el for el in os.listdir(log_dir) if os.path.isfile(os.path.join(log_dir, el))
    ]
    filedates = [None] * len(filenames)
    for ct, filename in enumerate(filenames):
        filedates[ct] = datetime.datetime.strptime(filename[:19], dt_frmt)
    remove_index = np.argsort(filedates)[: len(filedates) - keep_num]
    # Only show this message if its actually going to delete old logs

    if len(remove_index) > keep_num:
        logger.info("Running: Deleting old logs...")
    for r_ind in remove_index:
        os.remove(os.path.join(log_dir, filenames[r_ind]))
    if len(remove_index) > keep_num:
        logger.info("Success: Finished deleting old logs")


log_msg = start_logging("./log", info="scope", keep_num=10)
