import json
from typing import List, Dict, Any

def releases_to_json_summary(releases: List[Dict[str, Any]], indent: int = 2) -> str:
    """
    Given a list of releases (each with 'version_header' and 'notes'),
    output a JSON string summary.
    The output is a JSON array of objects:
      [
        {
          "version_header": "...",
          "notes": "..."
        },
        ...
      ]
    Args:
        releases: List of release dicts.
        indent: Indentation level for pretty-printing (default: 2).
    Returns:
        JSON string.
    """
    # Ensure all values are strings
    safe_releases = []
    for rel in releases:
        safe_releases.append({
            'version_header': str(rel.get('version_header', '')),
            'notes': str(rel.get('notes', ''))
        })
    return json.dumps(safe_releases, indent=indent, ensure_ascii=False)
