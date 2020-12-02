"""
Bactopia's parser entry-point.

Example: bactopia.parse(result_type, filename)
"""
import errno
import os
from typing import Union
from . import parsers
from .const import RESULT_TYPES


def parse(result_type: str, *files: str) -> Union[list, dict]:
    """
    Use the result type to automatically select the appropriate parsing method for an input.

    Args:
        result_type (str): the type of results (e.g. assembly, mlst, qc, etc...)
        *files (str): one or more input files to be parsed

    Raises:
        FileNotFoundError: the input file could not be found
        ValueError: the result type is not an accepted type

    Returns:
        Union[list, dict]: The results parsed for a given input.
    """
    if result_type in RESULT_TYPES:
        for f in files:
            if not os.path.exists(f):
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f)
        
        return getattr(parsers, result_type).parse(*files)
    else:
        raise ValueError(f"'{result_type}' is not an accepted result type. Accepted types: {', '.join(RESULT_TYPES)}")


def is_bactopia(path: str, name: str) -> list:
    """
    Check if a sample has any errors.

    Args:
        path (str): a path to expected Bactopia results
        name (str): the name of sample to test

    Returns:
        list: 0 (bool): path looks like Bactopia, 1 (list): any errors found
    """
    from .parsers.error import ERROR_TYPES
    errors = []
    is_bactopia = os.path.exists(f"{path}/{name}/{name}-genome-size.txt"")

    for error_type in ERROR_TYPES:
        filename = f"{path}/{name}/{name}-{error_type}-error.txt"
        if os.path.exists(filename):
            is_bactopia = True
            errors.append(parsers.error.parse(filename))

    return [is_bactopia, errors]
