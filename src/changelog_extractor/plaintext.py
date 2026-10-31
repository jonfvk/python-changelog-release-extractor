from typing import List, Dict, Any

def releases_to_plaintext_summary(releases: List[Dict[str, Any]]) -> str:
    """
    Given a list of releases (each with 'version_header' and 'notes'),
    output a plain text summary suitable for quick review.
    Each release is formatted as:

    <version_header>
    <notes>
    [blank line]
    ---
    [blank line]
    (No trailing --- after the last release)
    """
    lines = []
    for idx, rel in enumerate(releases):
        header = rel.get('version_header', '').strip()
        notes = rel.get('notes', '').strip()
        lines.append(header)
        if notes:
            lines.append(notes)
        # Add separator except after the last release
        if idx < len(releases) - 1:
            lines.append('')
            lines.append('---')
            lines.append('')
    return '\n'.join(lines).strip()
