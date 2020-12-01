"""
Parsers for BLAST related results.
"""
from .generic import get_file_type, parse_json
ACCEPTED_FILES = [".json", 'plsdb.txt']


def parse(filename: str) -> dict:
    """
    Check input file is an accepted file, then select the appropriate parsing method.

    Args:
        filename (str): input file to be parsed

    Returns:
        dict: parsed results
    """
    filetype = get_file_type(ACCEPTED_FILES, filename)
    if filetype == ".json":
        return _parse_blast(parse_json(filename))
    elif filetype == "plsdb.txt":
        return _parse_plsdb(filename)


def _parse_blast(jsondata: dict) -> dict:
    """
    Parse BLAST results and clean up final outputs.

    Args:
        jsondata (dict): the parsed BLAST results

    Returns:
        dict: BLAST results with reduced redundancy
    """
    results = {"program": None, 'queries': {}}
    for row in jsondata['BlastOutput2']:
        report = row['report']
        if not results["program"]:
            results['program'] = report['program']
            results['version'] = report['version']
            results['db'] = report['search_target']['db']
            results['params'] = report['params']

        search = report['results']['search']
        query_title = search['query_title']
        if query_title not in results['queries']:
            results['queries'][query_title] = {'query_len': search['query_len'], 'hits': [], 'message': ''}

        if search['hits']:
            for hit in search['hits']:
                results['queries'][query_title]['hits'].append({
                    'subject_title': hit['description'][0]['title'].split()[0],
                    'subject_len': hit['len'],
                    'hsps': hit['hsps']
                })
        
        if 'message' in search:
            results['queries'][query_title]['message'] = search['message']
    return results


def _parse_plsdb(filename: str) -> dict:
    """
    Correct PLSDB JSON format then use _parse_blast.

    Args:
        filename (str): PLSDB BLAST results to be parsed

    Returns:
        dict: the results in correct format
    """
    import json
    merged_json = None
    with open(filename, 'rt') as fh:
        entry = []
        entries = []
        for line in fh:
            entry.append(line)
            if line.startswith("}"):
                jsondata = json.loads(''.join(entry))
                if merged_json:
                    merged_json['BlastOutput2'].extend(jsondata['BlastOutput2'])
                else:
                    merged_json = jsondata
                entry.clear()
    return _parse_blast(merged_json)
