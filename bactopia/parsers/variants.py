"""
Parsers for Variant related results.
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
        return _parse_variants(filename)


def _parse_variants(filename: str) -> dict:
    """
    Parse Snippy summary text file.

    Args:
        filename (str): input file to be parsed

    Returns:
        dict: parsed Snippy summary file
    """
    from os.path import basename
    results = {}
    with open(filename, 'rt') as fh:
        for line in fh:
            line = line.rstrip()
            if not line.startswith("ReadFiles"):
                key, val = line.split("\t")
                if key == "Reference":
                    results[key] = basename(val).split('-')[-1].split(".")[0]
                else:
                    results[key] = val.lstrip()
    return results
