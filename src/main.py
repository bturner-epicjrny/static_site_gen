from copystatic import copy_dir_recursive
from generate_page import generate_page


def main():
    print("Copying static files to public...")
    copy_dir_recursive("static", "public")
    print("Static copy done.")

    print("Generating page...")
    generate_page("content/index.md", "template.html", "public/index.html")
    print("Page generation done.")


if __name__ == "__main__":
    main()
