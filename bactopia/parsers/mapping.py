from .generic import get_file_type
ACCEPTED_FILES = [".txt"]


def parse(filename):
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == ".txt":
        return _parse_mapping(filename)


def _parse_mapping(filename):
    """
    Parse per-base mapping summary text file. Example:

    ##total=1
    ##contig=<ID=lcl|NC_000907.1_cds_NP_438599.1_404,length=507>
    98
    104
    106
    107
    109
    112
    113
    113
    ...
    96
    95
    94

    """
    results = []
    with open(filename, 'rt') as fh:
        per_base_coverage = []
        name = None
        current_results = {}
        for line in fh:
            line = line.rstrip()
            if line:
                if line.startswith("##total"):
                    continue
                elif line.startswith("##contig"):
                    if name:
                        # This is not the first time
                        results.append({"name": name, "per_base_coverage": per_base_coverage})
                        per_base_coverage.clear()
                        name = None
                    name = line.replace("##", '')
                    print(name)
                else:
                    per_base_coverage.append(int(line))
            else:
                continue
        results.append({"name": name, "per_base_coverage": per_base_coverage})
    return results
