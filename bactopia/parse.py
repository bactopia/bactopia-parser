"""
Bactopia's parser entry-point.

Example: bactopia.parse(result_type, filename)
"""
import errno
import os
from collections import OrderedDict
from typing import Union
from . import parsers
from .const import RESULT_TYPES, IGNORE_LIST


def parse(result_type: str, *files: str) -> Union[list, dict]:
    """
    Use the result type to automatically select the appropriate parsing method for an input.

    Args:
        result_type (str): the type of results (e.g. assembly, mlst, qc, etc...)
        *files (str): one or more input files to be parsed

    Raises:
        FileNotFoundError: the input file could not be found
        ValueError: the result type is not an accepted type

    Returns:
        Union[list, dict]: The results parsed for a given input.
    """
    if result_type in RESULT_TYPES:
        for f in files:
            if not os.path.exists(f):
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), f)
        
        return getattr(parsers, result_type).parse(*files)
    else:
        raise ValueError(f"'{result_type}' is not an accepted result type. Accepted types: {', '.join(RESULT_TYPES)}")


def _is_bactopia_dir(path: str, name: str) -> list:
    """
    Check if a directory contains Bactopia output and any errors.

    Args:
        path (str): a path to expected Bactopia results
        name (str): the name of sample to test

    Returns:
        list: 0 (bool): path looks like Bactopia, 1 (list): any errors found
    """
    from .parsers.error import ERROR_TYPES
    errors = []
    is_bactopia = os.path.exists(f"{path}/{name}/{name}-genome-size.txt")

    for error_type in ERROR_TYPES:
        filename = f"{path}/{name}/{name}-{error_type}-error.txt"
        if os.path.exists(filename):
            is_bactopia = True
            errors.append(parsers.error.parse(filename))

    return [is_bactopia, errors]


def get_bactopia_files(path: str, name: str) -> dict:
    """
    Build a list of all parsable Bactopia files.

    Args:
        path (str): a path to expected Bactopia results
        name (str): the name of sample to test

    Raises:
        ValueError: The given directory is not a valid Bactopia dir

    Returns:
        dict: path and info on all parsable Bactopia files
    """
    path = os.path.abspath(os.path.expanduser(os.path.expandvars(path)))
    is_bactopia, errors = _is_bactopia_dir(path, name)
    bactopia_files = OrderedDict()
    bactopia_files['has_errors'] = True if errors else False
    bactopia_files['errors'] = errors
    bactopia_files['ignored'] = False
    bactopia_files['message'] = ""
    bactopia_files['files'] = OrderedDict()

    if is_bactopia:
        if not errors:
            bactopia_files['genome_size'] = f"{path}/{name}/{name}-genome-size.txt"
            for result_type in RESULT_TYPES:
                result_key = result_type
                if result_type == "amr":
                    result_key = "antimicrobial_resistance"
                elif result_type == "qc":
                    result_key = "quality-control"

                if result_type not in ['error', 'generic', 'kmers']:
                    bactopia_files['files'][result_key] = getattr(parsers, result_type).get_parsable_list(path, name)
    else:
        if name not in IGNORE_LIST:
            raise ValueError(f"'{path}/{name}' is not a valid Bactopia directory.")
        else:
            bactopia_files['ignored'] = True
            bactopia_files['message'] = f"'{path}/{name}' is on the Bactopia ignore list."

    return bactopia_files


def parse_bactopia_files(path: str, name: str) -> dict:
    """
    Parse all results associated with an input sample.

    Args:
        path (str): a path to expected Bactopia results
        name (str): the name of sample to test

    Returns:
        dict: The parsed set of results associated with the input sample
    """
    from bactopia.parsers.qc import is_paired
    bactopia_files = get_bactopia_files(path, name)
    bactopia_results = OrderedDict()
    bactopia_results['is_paired'] = None
    bactopia_results['has_errors'] = bactopia_files['has_errors']
    bactopia_results['errors'] = bactopia_files['errors']
    bactopia_results['has_missing'] = False
    bactopia_results['missing'] = []
    bactopia_results['ignored'] = bactopia_files['ignored']
    bactopia_results['message'] = bactopia_files['message']
    bactopia_results['results'] = OrderedDict()
    if not bactopia_files['has_errors'] and not bactopia_files['ignored']:
        for result_type, results in bactopia_files['files'].items():
            bactopia_results['is_paired'] = is_paired(path, name)
            bactopia_results['results'][result_type] = OrderedDict()
            result_key = result_type
            if result_type == "antimicrobial_resistance":
                result_key = "amr"
            elif result_type == "quality-control":
                result_key = "qc"
            
            for result in results:
                if result['missing']:
                    if not result['optional']:
                        bactopia_results['has_missing'] = True
                        bactopia_results['missing'].append([result_type, result["files"]])
                    else:
                        bactopia_results['results'][result_type][result['result_name']] = {}
                else:
                    bactopia_results['results'][result_type][result['result_name']] = parse(result_key, *result['files'])
            
    return bactopia_results


def parse_bactopia_directory(path: str) -> dict:
    """
    Scan a Bactopia directory and return parsed results.

    Args:
        path (str):  a path to expected Bactopia results

    Returns:
        dict: Parsed results for all samples in a Bactopia directory
    """
    from collections import defaultdict
    COUNTS = defaultdict(int)
    CATEGORIES = defaultdict(list)
    results = OrderedDict((
        ('categories', defaultdict(list)),
        ('counts', defaultdict(int)),
        ('samples', OrderedDict())
    ))

    with os.scandir(path) as dirs:
        for directory in dirs:
            if directory.name in IGNORE_LIST:
                results['counts']['ignore-list'] += 1
                results['categories']['ignore-list'].append(directory.name)
            else:
                sample_name = directory.name
                sample = parse_bactopia_files(path, sample_name)
                results['samples'][sample_name] = sample
                results['counts']['total'] += 1
                if sample['is_paired']:
                    results['counts']['paired-end'] += 1
                else:
                    results['counts']['single-end'] += 1

                if sample['has_errors']:
                    for error in sample['errors']:
                        results['counts'][error[0]] += 1
                        FAILED[error[0]].append(sample_name)
                    results['counts']['total-excluded'] += 1
                    results['counts']['qc-failure'] += 1
                    results['categories']['failed'].append([sample, f"Not processed, reason: {';'.join(sample['errors'])}"])
                
                if sample['has_missing']:
                    results['counts']['missing'] += 1
                    for missing in sample['missing']:
                        CATEGORIES['missing'].append([sample_name, missing[0], f"Missing expected files: {','.join(missing[1])}"])

                if not sample['has_errors'] and not sample['has_missing']:
                    results['counts']['processed'] += 1
                    results['categories']['processed'].append(sample_name)
            
    return results
