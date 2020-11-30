from .generic import get_file_type, parse_json
ACCEPTED_FILES = [".fna.json"]


def parse(filename):
    jsondata = None
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == ".fna.json":
        return {'assembly_stats': parse_json(filename)}
