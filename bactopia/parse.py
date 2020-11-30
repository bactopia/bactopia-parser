"""
Bactopia's parser entry-point.

Example: bactopia.parse(result_type, filename)
"""
import errno
import os
from . import parsers
from .const import RESULT_TYPES


def parse(result_type, filename):
    if result_type in RESULT_TYPES:
        if os.path.exists(filename):
            return getattr(parsers, result_type).parse(filename)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), filename)
    else:
        raise ValueError(f"'{result_type}' is not an accepted result type. Accepted types: {', '.join(RESULT_TYPES)}")
