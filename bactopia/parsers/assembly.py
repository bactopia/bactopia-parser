from .generic import get_file_type, parse_json, parse_table
ACCEPTED_FILES = [".fna.json", "checkm-results.txt"]


def parse(filename):
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == ".fna.json":
        return parse_json(filename)
    elif filetype == "checkm-results.txt":
        return parse_table(filename)[0]
