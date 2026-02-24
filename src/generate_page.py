import os
from pathlib import Path

from markdown_to_html_node import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.split("\n"):
        line = line.strip().lstrip("\ufeff")
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("no h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)

        if os.path.isfile(source_path):
            # only process markdown files
            if source_path.endswith(".md"):
                html_dest = str(Path(dest_path).with_suffix(".html"))
                generate_page(source_path, template_path, html_dest)
        else:
            # recurse into subdirectories
            generate_pages_recursive(source_path, template_path, dest_path)
