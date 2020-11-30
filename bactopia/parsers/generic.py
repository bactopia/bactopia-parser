

def get_file_type(extensions, name):
    """"""
    for ext in extensions:
        if name.endswith(ext):
            return ext

    raise ValueError(f"'{name}' is not an accepted result file. Accepted extensions: {', '.join(extensions)}")


def parse_table(csvfile, delimiter='\t', has_header=True):
    """Read a delimited file and return a list or dict depoending on presence of header."""
    import csv
    data = []
    with open(csvfile, 'rt') as fh:
        for row in csv.DictReader(fh, delimiter=delimiter) if has_header else csv.reader(fh, delimiter=delimiter):
            data.append(row)
    return data
