"""
Parsers for QC (FASTQ) related results.
"""
from .generic import get_file_type, parse_json
ACCEPTED_FILES = ["final.json", "original.json"]


def parse(r1: str, r2: str = None) -> dict:
    """
    Check input file is an accepted file, then select the appropriate parsing method.

    Args:
        r1 (str): input file associated with R1 or SE FASTQ
        r2 (str, optional): input file associated with R2 FASTQ. Defaults to None.

    Raises:
        ValueError: summary results to not have a matching origin (e.g. original vs final FASTQ)

    Returns:
        dict: parsed results
    """
    filetype = get_file_type(ACCEPTED_FILES, r1)
    filetype2 = filetype
    if r2:
        filetype2 = get_file_type(ACCEPTED_FILES, r2)

    if r1.endswith(".json"):
        if r2 and filetype != filetype2:
            raise ValueError(f"Original and Final QC files were mixed. R1: {filetype}, R2: {filetype2}")
        return _merge_qc_stats(parse_json(r1), parse_json(r2)) if r2 else parse_json(r1)


def _merge_qc_stats(r1: dict, r2: dict) -> dict:
    """
    Merge appropriate metrics (e.g. coverage) for R1 and R2 FASTQs.

    Args:
        r1 (dict): parsed metrics associated with R1 FASTQ
        r2 (dict): parsed metrics associated with R2 FASTQ

    Returns:
        dict: the merged FASTQ metrics
    """
    from statistics import mean
    merged = {
        'qc_stats': {},
        'r1_per_base_quality': r1['per_base_quality'],
        'r2_per_base_quality': r2['per_base_quality'],
        'r1_read_lengths': r1['read_lengths'],
        'r2_read_lengths': r2['read_lengths']
    }
    for key in r1['qc_stats']:
        if key in ['total_bp', 'coverage', 'read_total']:
            merged['qc_stats'][key] = r1['qc_stats'][key] + r2['qc_stats'][key] if r2 else r1['qc_stats'][key]
        else:
            val = mean([r1['qc_stats'][key], r2['qc_stats'][key]]) if r2 else r1['qc_stats'][key]
            merged['qc_stats'][key] = f'{val:.4f}' if isinstance(val, float) else val

    return merged
