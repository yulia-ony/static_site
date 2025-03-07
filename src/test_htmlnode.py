import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        expected_output = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected_output)
    
    def test_eq_tag(self):
        node = HTMLNode(tag="p")
        expected_output = "p"
        self.assertEqual(node.tag, expected_output)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)

    def test_eq_value(self):
        node = HTMLNode(value="the text inside a paragraph")
        expected_output = "the text inside a paragraph"
        self.assertEqual(node.value, expected_output)

    def test_repr(self):
        node = HTMLNode(tag="p", value="What a strange world", props={"class": "primary"},)
        self.assertEqual(node.__repr__(), "HTMLNode(p, What a strange world, None, {'class': 'primary'})",)

    def test_leaf_node_eq_value(self):
        node = LeafNode(tag="p", value="Here is some text")
        expected_output1 = "p"
        expected_output2 = "Here is some text"
        self.assertEqual(node.tag, expected_output1)
        self.assertEqual(node.value, expected_output2)

    def test_leaf_node_to_htms(self):
        node1 = LeafNode(tag="p", value="What a strange world")
        node2 = LeafNode(tag="a", value="Click here!", props={"href": "https://www.google.com"})
        node3 = LeafNode(tag=None, value="Just text")
        expected_output1 = "<p>What a strange world</p>"
        expected_output2 = '<a href="https://www.google.com">Click here!</a>'
        expected_output3 = "Just text"
        self.assertEqual(node1.to_html(), expected_output1)
        self.assertEqual(node2.to_html(), expected_output2)
        self.assertEqual(node3.to_html(), expected_output3)

    def test_parent_node_eq_value(self):
        node = ParentNode(tag="p", children=["a",], props={"href": "https://www.google.com"})
        expected_output1 = "p"
        expected_output2 = ["a"]
        expected_output3 = {"href": "https://www.google.com"}
        self.assertEqual(node.tag, expected_output1)
        self.assertEqual(node.children, expected_output2)
        self.assertEqual(node.props, expected_output3)
    
    def test_parent_node_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_node_to_html(self):
        node1 = ParentNode(tag="p", children=[])
        node2 = ParentNode(tag="a", children=[LeafNode(tag=None, value="Click here!")], props={"href": "https://www.google.com"})
        with self.assertRaises(ValueError) as context:
            node3 = ParentNode(tag=None, children=[LeafNode(tag=None, value="Click here!")], props={"href": "https://www.google.com"})
            node3.to_html()

        node4 = ParentNode(
            tag="a",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            props={"href": "https://www.google.com"},
        )

        expected_output1 = "<p></p>"
        expected_output2 = '<a href="https://www.google.com">Click here!</a>'
        expected_output4 = '<a href="https://www.google.com"><b>Bold text</b>Normal text<i>italic text</i>Normal text</a>'

        self.assertEqual(node1.to_html(), expected_output1)
        self.assertEqual(node2.to_html(), expected_output2)
        self.assertEqual(node4.to_html(), expected_output4)

if __name__ == "__main__":
    unittest.main()
