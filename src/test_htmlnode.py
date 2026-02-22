import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_new_obj_creation_without_params_are_None(self):
        node = HTMLNode()
        self.assertIs(node.tag, None)
        self.assertIs(node.value, None)
        self.assertIs(node.children, None)
        self.assertIs(node.props, None)

    def test_props_to_html_None(self):
        node = HTMLNode(tag="p", value="some text")
        self.assertIsNone(node.props_to_html())
    
    def test_props_to_html_one_prop_is_formatted(self):
        node = HTMLNode(props={ "href": "https://www.google.com", })
        self.assertEqual(node.props_to_html(), f"href=\"https://www.google.com\"")

    def test_props_to_html_multiple_props_is_formatted(self):
        node = HTMLNode(props={ "href": "https://www.google.com", "target": "_blank", })
        self.assertEqual(node.props_to_html(), f"href=\"https://www.google.com\" target=\"_blank\"")

if __name__ == "__main__":
    unittest.main()

