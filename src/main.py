import sys
from copystatic import copy_dir_recursive
from generate_page import generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    src = "static"
    dst = "docs"

    print("Copying static files...")
    copy_dir_recursive(src, dst)
    print("Static copy done.")

    print("Generating pages recursively...")
    generate_pages_recursive("content", "template.html", dst, basepath)
    print("Page generation done.")


if __name__ == "__main__":
    main()
