from .generic import get_file_type, parse_table
ACCEPTED_FILES = ["-gene-report.txt", "-protein-report.txt"]


def parse(filename):
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype.endswith("report.txt"):
        return (filename)


def _parse_amrfinder_report(filename):
    """Parse the AMRFinder report file."""
    return parse_table(filename)
