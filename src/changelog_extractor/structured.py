from typing import List, Dict, Any
from .release_notes import extract_release_notes
from .normalize import normalize_releases


def releases_to_structured_format(changelog_text: str) -> List[Dict[str, Any]]:
    """
    Parse the changelog text and return a structured list of releases.
    Each release is a dict with keys:
      - 'version_header': normalized header string
      - 'notes': normalized notes string
    """
    releases = extract_release_notes(changelog_text)
    structured = normalize_releases(releases)
    return structured
