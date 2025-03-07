import unittest
from markdown_to_html import markdown_to_html_node, extract_title

class TestMarkdownToHtml(unittest.TestCase):
    def test_heading_conversion(self):
        markdown = "# Heading 1"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "h1")
        self.assertEqual(node.children[0].children[0].value, "Heading 1")
    
    def test_paragraph_conversion(self):
        markdown = "This is a paragraph."
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].children[0].value, "This is a paragraph.")
    
    def test_unordered_list_conversion(self):
        markdown = "- Item 1\n- Item 2"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "ul")
        self.assertEqual(len(node.children[0].children), 2)
        self.assertEqual(node.children[0].children[0].tag, "li")
        self.assertEqual(node.children[0].children[0].children[0].value, "Item 1")
    
    def test_ordered_list_conversion(self):
        markdown = "1. First\n2. Second"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "ol")
        self.assertEqual(len(node.children[0].children), 2)
        self.assertEqual(node.children[0].children[0].tag, "li")
        self.assertEqual(node.children[0].children[0].children[0].value, "First")
    
    def test_blockquote_conversion(self):
        markdown = "> Quoted text"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "blockquote")
        self.assertEqual(node.children[0].children[0].value, "Quoted text")
    
    def test_code_block_conversion(self):
        markdown = "```\nCode block\n```"
        node = markdown_to_html_node(markdown)
        self.assertEqual(node.children[0].tag, "pre")
        self.assertEqual(node.children[0].children[0].tag, "code")
        self.assertEqual(node.children[0].children[0].children[0].value, "Code block")
    
    def test_single_title(self):
        markdown = [
            "# This is a title",
            "Some content",
            "More text"
        ]
        self.assertEqual(extract_title(markdown), "This is a title")

    def test_title_not_first_line(self):
        markdown = [
            "Some intro text",
            "# This is the title",
            "Another line"
        ]
        self.assertEqual(extract_title(markdown), "This is the title")

    def test_multiple_titles(self):
        markdown = [
            "# First title",
            "# Second title",
            "Some text"
        ]
        self.assertEqual(extract_title(markdown), "First title")

    def test_no_title(self):
        markdown = [
            "Some text",
            "More text",
            "Even more text"
        ]
        with self.assertRaises(ValueError) as context:
            extract_title(markdown)
        self.assertEqual(str(context.exception), "No title found in the markdown.")

    def test_title_with_extra_spaces(self):
        markdown = [
            "#   Title with spaces  ",
            "Other content"
        ]
        self.assertEqual(extract_title(markdown), "Title with spaces")

    def test_empty_list(self):
        markdown = []
        with self.assertRaises(ValueError):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()