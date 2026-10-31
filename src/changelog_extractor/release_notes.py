from typing import List, Dict, Any
from .release_header import find_release_headers


def extract_release_notes(changelog_text: str) -> List[Dict[str, Any]]:
    """
    Extract release notes under each release header.
    Returns a list of dicts: [{
        'version_header': str,  # The header line
        'notes': str           # The notes under this header (may be empty)
    }, ...]
    Notes are all lines after a header up to (but not including) the next header or end of file.
    """
    headers = find_release_headers(changelog_text)
    lines = changelog_text.splitlines()
    releases = []
    if not headers:
        return releases
    for idx, (header_idx, header_line) in enumerate(headers):
        # Start after the header line
        start = header_idx + 1
        # End at the next header or end of file
        if idx + 1 < len(headers):
            end = headers[idx + 1][0]
        else:
            end = len(lines)
        # Extract notes, strip leading/trailing blank lines
        notes_lines = lines[start:end]
        # Remove leading/trailing empty lines
        while notes_lines and notes_lines[0].strip() == '':
            notes_lines = notes_lines[1:]
        while notes_lines and notes_lines[-1].strip() == '':
            notes_lines = notes_lines[:-1]
        notes = '\n'.join(notes_lines)
        releases.append({
            'version_header': header_line,
            'notes': notes
        })
    return releases
