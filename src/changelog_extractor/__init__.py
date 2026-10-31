import os

class ChangelogExtractor:
    """
    ChangelogExtractor accepts a path to a changelog file.
    Provides methods to read file contents and get the file path.
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

    def read_file_contents(self):
        """
        Read and return the contents of the changelog file as a string.
        Raises FileNotFoundError if the file does not exist.
        Always reads with UTF-8 encoding.
        """
        if not os.path.isfile(self.changelog_path):
            raise FileNotFoundError(f"File not found: {self.changelog_path}")
        with open(self.changelog_path, "r", encoding="utf-8") as f:
            return f.read()
