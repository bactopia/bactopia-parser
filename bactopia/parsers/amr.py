from .generic import get_file_type, parse_table
ACCEPTED_FILES = ["-gene-report.txt", "-protein-report.txt"]

def parse(filename):
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == "-gene-report.txt":
        return _parse_gene_report(filename)
    else:
        return _parse_protein_report(filename)


def _parse_gene_report(filename):
    """Parse the AMR gene report file."""
    return {'gene-report': parse_table(filename)}


def _parse_protein_report(filename):
    """Parse the AMR protein report file."""
    return {'protein-report': parse_table(filename)}
