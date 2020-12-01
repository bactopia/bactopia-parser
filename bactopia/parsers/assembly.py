"""
Parsers for Assembly related results.
"""
from .generic import get_file_type, parse_json, parse_table
ACCEPTED_FILES = [".fna.json", "checkm-results.txt", "transposed_report.tsv"]


def parse(filename: str) -> dict:
    """
    Check input file is an accepted file, then select the appropriate parsing method.

    Args:
        filename (str): input file to be parsed

    Returns:
        dict: parsed results
    """
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == ".fna.json":
        return parse_json(filename)
    elif filetype == "checkm-results.txt" or filetype == "transposed_report.tsv":
        return parse_table(filename)[0]
