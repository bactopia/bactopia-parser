"""
Parsers for Annotation related results.
"""
from .generic import get_file_type
ACCEPTED_FILES = [".txt"]


def parse(filename: str) -> dict:
    """
    Check input file is an accepted file, then select the appropriate parsing method.

    Args:
        filename (str): input file to be parsed

    Returns:
        dict: parsed results
    """
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == ".txt":
        return _parse_annotation(filename)


def _parse_annotation(filename: str) -> dict:
    """
    Parse Prokka summary text file.

    Args:
        filename (str): input file to be parsed

    Returns:
        dict: the parsed Prokka summary
    """
    results = {}
    with open(filename, 'rt') as fh:
        for line in fh:
            line = line.rstrip()
            key, val = line.split(":")
            results[key] = val.lstrip()
    return results
