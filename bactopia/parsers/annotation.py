from .generic import get_file_type
ACCEPTED_FILES = [".txt"]


def _parse_annotation(filename):
    """Parse Prokka summary text file."""
    results = {}
    with open(filename, 'rt') as fh:
        for line in fh:
            line = line.rstrip()
            key, val = line.split(":")
            results[key] = val.lstrip()
    return results


def parse(filename):
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == ".txt":
        return _parse_annotation(filename)
