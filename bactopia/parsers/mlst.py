from .generic import get_file_type, parse_json, parse_table
ACCEPTED_FILES = ["blast.json", "mlst_report.tsv"]


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
    if filetype == "blast.json":
        return parse_json(filename)
    elif filetype == "mlst_report.tsv":
        return parse_table(filename)[0]
