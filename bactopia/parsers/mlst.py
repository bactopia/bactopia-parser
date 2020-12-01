"""
Parsers for MLST related results.
"""
from .generic import get_file_type, parse_json, parse_table
ACCEPTED_FILES = ["blast.json", "mlst_report.tsv"]


def parse(filename: str) -> dict:
    """
    Check input file is an accepted file, then select the appropriate parsing method.

    Args:
        filename (str): input file to be parsed

    Returns:
        dict: parsed results
    """
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == "blast.json":
        return parse_json(filename)
    elif filetype == "mlst_report.tsv":
        return parse_table(filename)[0]
