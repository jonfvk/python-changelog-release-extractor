import re
from typing import List, Dict, Any

def normalize_release_header(header: str) -> str:
    """
    Normalize a release header line to a consistent format:
      - Remove extra spaces
      - Standardize dashes (hyphen, en dash, em dash) to hyphen
      - Ensure version is bracketed: [1.0.0]
      - Date is formatted as YYYY-MM-DD if present
    Returns the normalized header string.
    """
    # Replace en dash/em dash with hyphen
    header = re.sub(r'[–—]', '-', header)
    # Remove duplicate spaces
    header = re.sub(r'\s+', ' ', header).strip()
    # Extract version and date
    m = re.match(r'^##\s*\[?(v?\d+\.\d+(?:\.\d+)?(?:[-\w]*)?)\]?\s*[-\( ]*([0-9]{4}-[0-9]{2}-[0-9]{2})?\)?', header)
    if m:
        version = m.group(1)
        date = m.group(2)
        if version:
            version = version.lstrip('v')
        norm = f"## [{version}]"
        if date:
            norm += f" - {date}"
        return norm
    return header

def normalize_release_notes(notes: str) -> str:
    """
    Normalize release notes:
      - Convert all bullet points to '-'
      - Remove trailing spaces
      - Replace tabs with 2 spaces
      - Remove duplicate blank lines
    """
    lines = notes.splitlines()
    norm_lines = []
    prev_blank = False
    for line in lines:
        orig = line
        line = line.replace('\t', '  ')
        # Normalize bullets: *, +, - to '-'
        bullet = re.match(r'^(\s*)([\-*+])\s+', line)
        if bullet:
            indent = bullet.group(1)
            line = re.sub(r'^(\s*)[\-*+]\s+', f'{indent}- ', line)
        line = line.rstrip()
        if line == '':
            if prev_blank:
                continue  # skip duplicate blank lines
            prev_blank = True
        else:
            prev_blank = False
        norm_lines.append(line)
    return '\n'.join(norm_lines).strip()

def normalize_releases(releases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Given a list of releases (with 'version_header' and 'notes'),
    normalize their formatting.
    """
    norm = []
    for rel in releases:
        norm.append({
            'version_header': normalize_release_header(rel['version_header']),
            'notes': normalize_release_notes(rel['notes'])
        })
    return norm
