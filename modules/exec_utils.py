"""
Exec eval utilities.
"""

import logging
import os
import time

from contextlib import contextmanager
from typing import Optional, Union

HDLR_LEVEL = Union[str, int]


def get_logger(stream_hdlr_level: HDLR_LEVEL = 'INFO',
               file_hdlr_level: HDLR_LEVEL = 'INFO',
               out_file: Optional[Union[str, bytes, os.PathLike]] = None) -> logging.Logger:
    r"""Set up stream and file handlers for current logger.

    Parameters
    ----------
    stream_hdlr_level: str, int
        Stream handler logging level.
    file_hdlr_level: str, int
        File handler logging level.
    out_file: path-like, optional
        Specify where the file handler saves log. No file handler is set up if
        set to ``None``. Default is ``None``.

    Returns
    -------
    logger: logging.Logger
        The current logger with handlers set up.

    """
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    logger.handlers = []
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(stream_hdlr_level)
    logger.addHandler(handler)

    if out_file is not None:
        fh = logging.FileHandler(out_file)
        fh.setFormatter(formatter)
        fh.setLevel(file_hdlr_level)
        logger.addHandler(fh)
    logger.info('logger set up')

    return logger


@contextmanager
def timer(name: str, logger: Optional[logging.Logger] = None):
    """A decorator which measures the execute time of the codes.

    Parameters
    ----------
    name : str
        Specify a name for the timer.
    logger : logging.Logger, optional
        Specify the logger where the timer messages are redirected to. Messages
        will be shown with ``print`` function if set to ``None``. Default is
        ``None``.

    Examples
    --------
    >>> with timer('Processing something', logger):
    >>>     # Codes to be measured the execute time.
    >>>     pass

    """
    t0 = time.time()
    msg = f'[{name}] start'
    if logger is None:
        print(msg)
    else:
        logger.info(msg)
    yield

    msg = f'[{name}] done in {time.time() - t0:.2f} s'
    if logger is None:
        print(msg)
    else:
        logger.info(msg)

