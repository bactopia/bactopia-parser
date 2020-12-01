from .generic import get_file_type
ACCEPTED_FILES = [".txt"]


def parse(filename):
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == ".txt":
        return _parse_variants(filename)


def _parse_variants(filename):
    """Parse Snippy summary text file."""
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
