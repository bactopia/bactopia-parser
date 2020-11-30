"""
Bactopia's parser entry-point.

Example: bactopia.parse(result_type, filename)
"""
import errno
import os
from . import parsers
from .const import RESULT_TYPES


def parse(result_type, *files):
    if result_type in RESULT_TYPES:
        for f in files:
            if not os.path.exists(f):
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f)
        
        return getattr(parsers, result_type).parse(*files)
    else:
        raise ValueError(f"'{result_type}' is not an accepted result type. Accepted types: {', '.join(RESULT_TYPES)}")
