# markdown_to_html_node.py

from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType
from text_to_textnodes import text_to_textnodes
from text_node_to_html_node import text_node_to_html_node
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


def text_to_children(text):
    """
    Convert inline markdown text into a list of HTMLNodes.
    Uses your existing inline parsing pipeline:
    raw text -> TextNodes -> LeafNodes
    """
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []

    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(block_to_html_node(block, block_type))

    return ParentNode("div", children)


def block_to_html_node(block, block_type):
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)

    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)

    if block_type == BlockType.CODE:
        return code_to_html_node(block)

    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)

    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)

    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)

    raise ValueError("unknown block type")


def paragraph_to_html_node(block):
    # Replace internal newlines with spaces
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    # Count leading #'s
    level = 0
    while level < len(block) and block[level] == "#":
        level += 1

    # Skip "#... " prefix
    text = block[level + 1 :]  # assumes valid heading format "# "
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    # block looks like:
    # ```
    # code here
    # ```
    # remove opening "```\n" and closing "```"
    code_text = block[4:-3]

    # Preserve text exactly; no inline parsing for code blocks
    code_leaf = text_node_to_html_node(TextNode(code_text, TextType.CODE))
    return ParentNode("pre", [code_leaf])


def quote_to_html_node(block):
    lines = block.split("\n")
    cleaned = []

    for line in lines:
        # line starts with ">"
        content = line[1:]
        if content.startswith(" "):
            content = content[1:]
        cleaned.append(content)

    # For quote blocks, combine lines with spaces (similar to paragraphs)
    text = " ".join(cleaned)
    return ParentNode("blockquote", text_to_children(text))


def unordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []

    for line in lines:
        # line starts with "- "
        item_text = line[2:]
        items.append(ParentNode("li", text_to_children(item_text)))

    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    lines = block.split("\n")
    items = []

    for line in lines:
        # Remove "<number>. " prefix
        dot_index = line.find(".")
        item_text = line[dot_index + 2 :]
        items.append(ParentNode("li", text_to_children(item_text)))

    return ParentNode("ol", items)
