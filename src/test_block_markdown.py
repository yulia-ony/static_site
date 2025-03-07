import unittest
from block_markdown import markdown_to_blocks, block_to_block_type

class TestMarkdownToBlocks(unittest.TestCase):

    def test_basic_case(self):
        markdown = "This is paragraph one.\n\nThis is paragraph two."
        expected = ["This is paragraph one.", "This is paragraph two."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_leading_trailing_whitespace(self):
        markdown = "  This is a test.  \n\n  Another test.  "
        expected = ["This is a test.", "Another test."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_consecutive_newlines(self):
        markdown = "First paragraph.\n\n\n\nSecond paragraph.\n\n\n\nThird paragraph."
        expected = ["First paragraph.", "Second paragraph.", "Third paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_single_line_input(self):
        markdown = "Single paragraph with no breaks."
        expected = ["Single paragraph with no breaks."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_input(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_mixed_newline_formats(self):
        markdown = "Line1.\n \n \nLine2.\n\n   Line3."
        expected = ["Line1.", "Line2.", "Line3."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("# Heading"), "heading")
        self.assertEqual(block_to_block_type("## Subheading"), "heading")
        self.assertEqual(block_to_block_type("```code\nprint('Hello')\n```"), "code")
        self.assertEqual(block_to_block_type("> Quote\n> Line 2"), "quote")
        self.assertEqual(block_to_block_type("* Item 1\n* Item 2"), "unordered_list")
        self.assertEqual(block_to_block_type("1. First\n2. Second"), "ordered_list")
        self.assertEqual(block_to_block_type("This is a paragraph."), "paragraph")

if __name__ == "__main__":
    unittest.main()