from .generic import get_file_type, parse_json
ACCEPTED_FILES = ["final.json", "original.json"]


def parse(r1, r2=None):
    jsondata = None
    filetype = get_file_type(ACCEPTED_FILES, r1)
    filetype2 = filetype
    if r2:
        filetype2 = get_file_type(ACCEPTED_FILES, r2)

    if r1.endswith(".json"):
        if r2 and filetype != filetype2:
            raise ValueError(f"Original and Final QC files were mixed. R1: {filetype}, R2: {filetype2}")
        return _parse_json(r1, r2)


def _parse_json(r1, r2):
    """Return a dict of QC stats."""
    return = _merge_qc_stats(parse_json(r1), parse_json(r2)) if r2 else parse_json(r1)


def _merge_qc_stats(r1, r2):
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
