import logging
from pathlib import Path

from pytorch_lightning.utilities import rank_zero_only
from hydra_zen import to_yaml


def get_pylogger(name=__name__) -> logging.Logger:
    """Initializes multi-GPU-friendly python command line logger."""

    logger = logging.getLogger(name)

    # this ensures all logging levels get marked with the rank zero decorator
    # otherwise logs would get multiplied for each GPU process in multi-GPU setup
    logging_levels = (
        "debug",
        "info",
        "warning",
        "error",
        "exception",
        "fatal",
        "critical",
    )
    for level in logging_levels:
        setattr(logger, level, rank_zero_only(getattr(logger, level)))

    return logger


def print_file(x: Path):
    """Prints the contents of a file to the command line.

    Args:
        x (Path): Path to file.
    """
    with x.open("r") as f:
        print(f.read())


def print_yaml(x):
    print(to_yaml(x))
