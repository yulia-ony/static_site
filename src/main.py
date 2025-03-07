from textnode import TextNode, TextType
from copystatic import copy_static_to_public
from generatepage import generate_pages_recursive
import os


STATIC_DIR = "./static"
PUBLIC_DIR = "./public"
CONTENT_DIR = "./content"
TEMPLATE_PATH = "./template.html"

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)

    copy_static_to_public(source=STATIC_DIR, destination=PUBLIC_DIR)

    os.makedirs(PUBLIC_DIR, exist_ok=True)

    print("Generating page...")
    generate_pages_recursive(CONTENT_DIR, TEMPLATE_PATH, PUBLIC_DIR)

    
if __name__ == "__main__":
    main()
