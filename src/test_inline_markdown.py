import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link 


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_delimiter(self):
        node = TextNode("This has **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result,
            [
                TextNode("This has ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_italic_delimiter(self):
        node = TextNode("An _italic_ word", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            result,
            [
                TextNode("An ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_unchanged(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [node])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("Hello ", TextType.TEXT),
            TextNode("`code`", TextType.TEXT),
            TextNode(" world", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(
            result,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" world", TextType.TEXT),
            ],
        )

    def test_unmatched_delimiter_raises(self):
        node = TextNode("This is `broken", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches
        )

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "![rick](https://a.com/r.gif) and ![obi](https://b.com/o.jpeg)"
        )
        self.assertListEqual(
            [("rick", "https://a.com/r.gif"), ("obi", "https://b.com/o.jpeg")],
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "A [link](https://boot.dev) here"
        )
        self.assertListEqual(
            [("link", "https://boot.dev")],
            matches
        )

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "Visit [Boot.dev](https://www.boot.dev) and [YouTube](https://youtube.com)"
        )
        self.assertListEqual(
            [("Boot.dev", "https://www.boot.dev"), ("YouTube", "https://youtube.com")],
            matches
        )

    def test_links_does_not_match_images(self):
        matches = extract_markdown_links(
            "![img](https://img.com/x.png) and [site](https://example.com)"
        )
        self.assertListEqual(
            [("site", "https://example.com")],
            matches
        )


class TestSplitImagesAndLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_images_no_images(self):
        node = TextNode("just text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_links_no_links(self):
        node = TextNode("just text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_non_text_nodes_unchanged_image(self):
        node = TextNode("bold", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_non_text_nodes_unchanged_link(self):
        node = TextNode("code", TextType.CODE)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_image_at_start_and_end(self):
        node = TextNode(
            "![a](https://a.com)x![b](https://b.com)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://a.com"),
                TextNode("x", TextType.TEXT),
                TextNode("b", TextType.IMAGE, "https://b.com"),
            ],
            split_nodes_image([node]),
        )

    def test_link_at_start_and_end(self):
        node = TextNode(
            "[a](https://a.com)x[b](https://b.com)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode("x", TextType.TEXT),
                TextNode("b", TextType.LINK, "https://b.com"),
            ],
            split_nodes_link([node]),
        )        