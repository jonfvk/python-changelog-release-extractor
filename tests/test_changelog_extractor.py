import os
import unittest
import tempfile
from src.changelog_extractor import ChangelogExtractor

class TestChangelogExtractor(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and file for the changelog
        self.temp_dir = tempfile.TemporaryDirectory()
        self.changelog_content = (
            """# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n## [1.0.0] - 2024-06-01\n- Initial release.\n\n## [0.9.0] - 2024-05-20\n- Beta release.\n"""
        )
        self.changelog_path = os.path.join(self.temp_dir.name, "CHANGELOG.md")
        with open(self.changelog_path, "w", encoding="utf-8") as f:
            f.write(self.changelog_content)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_get_changelog_path(self):
        extractor = ChangelogExtractor(self.changelog_path)
        self.assertEqual(extractor.get_changelog_path(), self.changelog_path)

    def test_read_file_contents(self):
        extractor = ChangelogExtractor(self.changelog_path)
        contents = extractor.read_file_contents()
        self.assertEqual(contents, self.changelog_content)

    def test_read_file_contents_file_not_found(self):
        extractor = ChangelogExtractor(os.path.join(self.temp_dir.name, "NOFILE.md"))
        with self.assertRaises(FileNotFoundError):
            extractor.read_file_contents()

    def test_read_file_contents_encoding(self):
        # Write a file with non-ASCII content
        content = "## [2.0.0] – 2024-07-01\n– Añadido soporte para español.\n"
        path = os.path.join(self.temp_dir.name, "CHANGELOG_ES.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        extractor = ChangelogExtractor(path)
        self.assertEqual(extractor.read_file_contents(), content)

if __name__ == "__main__":
    unittest.main()
