import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        # If there are an even number of parts, delimiters are unmatched
        # Example: "hello `code" -> ["hello ", "code"]  (2 parts => invalid)
        if len(parts) % 2 == 0:
            raise Exception(f"invalid markdown syntax: unmatched delimiter '{delimiter}'")

        for i, part in enumerate(parts):
            if part == "":
                continue  # skip empty segments

            if i % 2 == 0:
                # outside delimiters
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                # inside delimiters
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)

        if len(images) == 0:
            new_nodes.append(node)
            continue

        remaining = text
        for alt, url in images:
            markdown_image = f"![{alt}]({url})"
            sections = remaining.split(markdown_image, 1)

            if len(sections) != 2:
                raise Exception("invalid markdown image syntax")

            before, after = sections

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = after

        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining = text
        for anchor, url in links:
            markdown_link = f"[{anchor}]({url})"
            sections = remaining.split(markdown_link, 1)

            if len(sections) != 2:
                raise Exception("invalid markdown link syntax")

            before, after = sections

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining = after

        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes    