import unittest
from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        md = "# Hello"
        self.assertEqual(extract_title(md), "Hello")

    def test_extract_title_with_whitespace(self):
        md = "   #   Hello World   "
        self.assertEqual(extract_title(md), "Hello World")

    def test_extract_title_from_multiline(self):
        md = """
Some intro text

# Tolkien Fan Club

More text
"""
        self.assertEqual(extract_title(md), "Tolkien Fan Club")

    def test_extract_title_ignores_h2(self):
        md = "## Not an h1"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_missing_raises(self):
        md = "No heading here"
        with self.assertRaises(Exception):
            extract_title(md)
