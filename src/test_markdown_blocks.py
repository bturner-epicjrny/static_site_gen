import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_input(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_extra_blank_lines(self):
        md = "A\n\n\n\nB"
        self.assertEqual(markdown_to_blocks(md), ["A", "B"])

    def test_whitespace_trimmed(self):
        md = "   A block   \n\n   Another block   "
        self.assertEqual(markdown_to_blocks(md), ["A block", "Another block"])

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Hello"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Hello"), BlockType.HEADING)

    def test_code(self):
        block = "```\nprint('hi')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = "> quote\n>more"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- one\n- two\n- three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. one\n2. two\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = "Just a normal paragraph\nwith two lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        