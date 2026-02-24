from enum import Enum
import re

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    result = []

    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            result.append(stripped)

    return result

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    # Heading: 1-6 #'s, then a space
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Code block: starts with ```\n and ends with ```
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    # Quote block: every line starts with >
    if len(lines) > 0 and all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list: every line starts with "- "
    if len(lines) > 0 and all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list: each line starts with "1. ", "2. ", ...
    ordered = True
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            ordered = False
            break
    if ordered and len(lines) > 0:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
