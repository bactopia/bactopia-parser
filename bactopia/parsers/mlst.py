from .generic import get_file_type, parse_json, parse_table
ACCEPTED_FILES = ["blast.json", "mlst_report.tsv"]


def parse(filename):
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == "blast.json":
        return parse_json(filename)
    elif filetype == "mlst_report.tsv":
        return parse_table(filename)[0]
