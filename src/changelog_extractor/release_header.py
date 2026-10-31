import re
from typing import List, Tuple

def find_release_headers(changelog_text: str) -> List[Tuple[int, str]]:
    """
    Identify release headers in the changelog text.
    Returns a list of tuples: (line_number, header_line)
    A release header is a line that matches common version/date patterns, e.g.:
      ## [1.0.0] - 2024-06-01
      ## 1.0.0 (2024-06-01)
      ## [0.9.0]
    """
    header_pattern = re.compile(
        r"^##\s*\[?(v?\d+\.\d+(?:\.\d+)?(?:[-\w]*)?)\]?"  # version
        r"(?:\s*[-–—]\s*|\s*\(|\s+)?"                      # separator
        r"(\d{4}-\d{2}-\d{2})?"                             # optional date
        r"[) ]*"                                               # closing paren or space
        , re.IGNORECASE
    )
    headers = []
    for idx, line in enumerate(changelog_text.splitlines()):
        if header_pattern.match(line.strip()):
            headers.append((idx, line.strip()))
    return headers
