from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)
        
        print(f"Processing text: {old_node.text}")
        print(f"Sections split by {delimiter}: {sections}")

        if len(sections) % 2 == 0:
            print(f"Error: Unmatched delimiter {delimiter} in: {old_node.text}")
            raise ValueError(f"Invalid markdown, {delimiter} section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        matches = extract_markdown_images(text)
        if not matches:
            new_nodes.append(old_node)
            continue
        
        while matches:
            match = matches.pop(0)
            parts = re.split(r"!\[.*?\]\(.*?\)", text, maxsplit=1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.IMAGE, match[1]))
            text = parts[1] if len(parts) > 1 else ""
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        text = old_node.text
        matches = extract_markdown_links(text)
        if not matches:
            new_nodes.append(old_node)
            continue
        
        while matches:
            match = matches.pop(0)
            parts = re.split(r"\[.*?\]\(.*?\)", text, maxsplit=1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(match[0], TextType.LINK, match[1]))
            text = parts[1] if len(parts) > 1 else ""
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    try:
        old_nodes = [TextNode(text=text, text_type=TextType.TEXT)]
        
        # Process delimiters carefully to handle mixed formatting
        old_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)  # Code first
        old_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)  # Bold second
        old_nodes = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)  # Italic last
        old_nodes = split_nodes_image(old_nodes)
        old_nodes = split_nodes_link(old_nodes)
        
        return old_nodes
    except ValueError as e:
        print(f"Error in text_to_textnodes processing: {text}")
        raise e

