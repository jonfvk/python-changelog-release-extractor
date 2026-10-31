import os

class ChangelogExtractor:
    """
    ChangelogExtractor accepts a path to a changelog file.
    Future milestones will implement parsing and extraction logic.
    """
    def __init__(self, changelog_path):
        if not isinstance(changelog_path, str):
            raise TypeError("changelog_path must be a string")
        self.changelog_path = changelog_path

    def get_changelog_path(self):
        """
        Return the stored changelog file path.
        """
        return self.changelog_path
