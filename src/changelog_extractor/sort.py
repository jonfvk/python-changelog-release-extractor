import re
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

def _parse_version(version: str) -> Tuple:
    """
    Parse a version string into a tuple for sorting.
    Handles semantic versions like 1.2.3, 1.2, 1.2.3-beta, etc.
    Non-numeric suffixes are sorted after numeric versions.
    """
    # Remove leading 'v' if present
    version = version.lstrip('v')
    # Split version and suffix (e.g., 1.2.3-beta)
    m = re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?(?:[-_]([\w.]+))?$', version)
    if not m:
        # Fallback: treat as string
        return (version,)
    major = int(m.group(1))
    minor = int(m.group(2))
    patch = int(m.group(3)) if m.group(3) else 0
    suffix = m.group(4) or ''
    return (major, minor, patch, suffix)

def _extract_version_and_date(header: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Extract version and date from a normalized release header.
    Example: '## [1.0.0] - 2024-06-01' -> ('1.0.0', '2024-06-01')
    """
    m = re.match(r'^## \[(v?\d+\.\d+(?:\.\d+)?(?:[-\w]*)?)\](?: - (\d{4}-\d{2}-\d{2}))?', header)
    if m:
        version = m.group(1)
        date = m.group(2)
        return version, date
    return None, None

def _parse_date(date_str: Optional[str]) -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None

def sort_releases_chronologically(releases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sorts a list of releases chronologically (most recent first).
    If dates are present, sort by date descending.
    If no date, sort by version descending (semantic version order).
    Releases with no date or version are sorted last.
    """
    def sort_key(rel):
        version, date = _extract_version_and_date(rel.get('version_header', ''))
        dt = _parse_date(date)
        version_tuple = _parse_version(version) if version else ()
        # Releases with date come first, then by version, then others
        # For descending order: newer date/version first
        # Use negative timestamp for descending date
        if dt:
            return (0, -dt.timestamp(), version_tuple)
        elif version_tuple:
            return (1, (), version_tuple)
        else:
            return (2, (), ())
    return sorted(releases, key=sort_key)
