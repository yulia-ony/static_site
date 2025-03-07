from textnode import TextNode, TextType
from copystatic import copy_static_to_public
from generatepage import generate_pages_recursive
import os
import sys


STATIC_DIR = "./static"
PUBLIC_DIR = "./docs"
CONTENT_DIR = "./content"
TEMPLATE_PATH = "./template.html"

def main():
    # Read CLI argument for basepath, default to "/"
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Using basepath: {basepath}")

    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)

    copy_static_to_public(source=STATIC_DIR, destination=PUBLIC_DIR)

    os.makedirs(PUBLIC_DIR, exist_ok=True)

    print("Generating pages...")
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, PUBLIC_DIR, basepath)

if __name__ == "__main__":
    main()
