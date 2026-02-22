import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_p_props(self):
        node = LeafNode("p", "Hello, world!", {"class": "headerContent",})
        self.assertEqual(node.to_html(), "<p class=\"headerContent\">Hello, world!</p>")
    
    def test_leaf_to_html_value_only(self):
        node = LeafNode(None, "just a value")
        self.assertEqual(node.to_html(), "just a value")


if __name__ == "__main__":
    unittest.main()

