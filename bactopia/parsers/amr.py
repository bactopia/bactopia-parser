"""
Parsers for Antimicrobial Resistance related results.
"""
from .generic import get_file_type, parse_table
ACCEPTED_FILES = ["-gene-report.txt", "-protein-report.txt"]


def parse(filename: str) -> dict:
    """
    Check input file is an accepted file, then select the appropriate parsing method.

    Args:
        filename (str): input file to be parsed

    Returns:
        dict: parsed results
    """
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype.endswith("report.txt"):
        return (filename)


def _parse_amrfinder_report(filename: str) -> dict:
    """
    Parse the AMRFinder report file.

    Args:
        filename (str): input file to be parsed

    Returns:
        dict: the parsed AMRFinder+ results
    """
    return parse_table(filename)
