"""
Parsers for Ariba related results.
"""
from .generic import get_file_type, parse_json, parse_table
ACCEPTED_FILES = ["report.tsv", "summary.csv"]


def parse(report_file: str, summary_file: str) -> dict:
    """
    Check input file is an accepted file, then select the appropriate parsing method.

    Args:
        report_file (str): An Ariba report file of clusters which passed filtering.
        summary_file (str): A summary file of the report

    Returns:
        dict: the parsed results
    """
    filetype = get_file_type(ACCEPTED_FILES, report_file)
    filetype2 = get_file_type(ACCEPTED_FILES, summary_file)
    if filetype == "report.tsv" and filetype2 == "summary.csv":
        return _parse_ariba(report_file, summary_file)


def _parse_ariba(report_file: str, summary_file: str) -> dict:
    """
    Parse the results of Ariba.

    Args:
        report_file (str): An Ariba report file of clusters which passed filtering.
        summary_file (str): A summary file of the report

    Returns:
        dict: the parsed Ariba results with modifed summary format
    """
    # Fix up the summary
    hits = {}
    for row in parse_table(summary_file, delimiter=","):
        for key, val in row.items():
            if key != 'name':
                cluster, field = key.split('.')
                if cluster not in hits:
                    hits[cluster] = {
                        'cluster': cluster,
                    }
                hits[cluster][field] = val

    summary = []
    for cluster, vals in sorted(hits.items()):
        summary.append(vals)

    return {'report': parse_table(report_file), 'summary': summary}
