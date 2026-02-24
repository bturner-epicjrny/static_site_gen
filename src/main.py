from copystatic import copy_dir_recursive
from generate_page import generate_pages_recursive


def main():
    print("Copying static files to public...")
    copy_dir_recursive("static", "public")
    print("Static copy done.")

    print("Generating pages recursively...")
    generate_pages_recursive("content", "template.html", "public")
    print("Page generation done.")


if __name__ == "__main__":
    main()
