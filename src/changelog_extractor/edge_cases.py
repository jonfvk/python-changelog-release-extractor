import re
from typing import List, Dict, Any, Optional
from .release_header import find_release_headers
from .normalize import normalize_release_header, normalize_release_notes


def find_unreleased_section(changelog_text: str) -> Optional[Dict[str, Any]]:
    """
    Detect and extract an 'Unreleased' section if present.
    Returns a dict with keys:
      - 'version_header': str (e.g., '## [Unreleased]')
      - 'notes': str (notes under this section)
    or None if not found.
    Recognizes common patterns:
      ## [Unreleased]
      ## Unreleased
      ## [Next]
    """
    lines = changelog_text.splitlines()
    unreleased_pattern = re.compile(r'^##\s*\[?(Unreleased|Next)\]?', re.IGNORECASE)
    for idx, line in enumerate(lines):
        if unreleased_pattern.match(line.strip()):
            # Find the next release header (if any)
            headers = find_release_headers('\n'.join(lines[idx+1:]))
            if headers:
                end = idx + 1 + headers[0][0]
            else:
                end = len(lines)
            # Extract notes
            notes_lines = lines[idx+1:end]
            # Remove leading/trailing blank lines
            while notes_lines and notes_lines[0].strip() == '':
                notes_lines = notes_lines[1:]
            while notes_lines and notes_lines[-1].strip() == '':
                notes_lines = notes_lines[:-1]
            notes = '\n'.join(notes_lines)
            return {
                'version_header': normalize_release_header(line.strip()),
                'notes': normalize_release_notes(notes)
            }
    return None


def extract_all_releases_with_edge_cases(changelog_text: str) -> List[Dict[str, Any]]:
    """
    Extract all releases, including any 'Unreleased' section if present.
    Returns a list of dicts: [{
        'version_header': str,
        'notes': str
    }, ...]
    The 'Unreleased' section (if present) is always first.
    """
    from .release_notes import extract_release_notes
    from .normalize import normalize_releases
    releases = []
    unreleased = find_unreleased_section(changelog_text)
    if unreleased:
        releases.append(unreleased)
    # Remove the unreleased section from the text for further parsing
    if unreleased:
        # Remove lines from the start of the unreleased header to the start of the next header
        lines = changelog_text.splitlines()
        unreleased_pattern = re.compile(r'^##\s*\[?(Unreleased|Next)\]?', re.IGNORECASE)
        start_idx = None
        for idx, line in enumerate(lines):
            if unreleased_pattern.match(line.strip()):
                start_idx = idx
                break
        if start_idx is not None:
            # Find the next release header
            headers = find_release_headers('\n'.join(lines[start_idx+1:]))
            if headers:
                end_idx = start_idx + 1 + headers[0][0]
            else:
                end_idx = len(lines)
            # Remove unreleased section
            lines = lines[:start_idx] + lines[end_idx:]
            changelog_text = '\n'.join(lines)
    # Extract the rest
    rest = extract_release_notes(changelog_text)
    releases.extend(normalize_releases(rest))
    return releases
