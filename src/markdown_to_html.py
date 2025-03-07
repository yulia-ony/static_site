import re
from htmlnode import ParentNode
from block_markdown import block_to_block_type, markdown_to_blocks
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        try:
            print(f"\nProcessing block:\n{block}\n")
            block_type = block_to_block_type(block)
            print(f"Block type detected: {block_type}")
        except Exception as e:
            print(f"Error detecting block type for:\n{block}")
            raise e
        
        if block_type == "heading":
            level = len(re.match(r'^(#{1,6}) ', block).group(1))
            text = block[level + 1:].strip()
            block_nodes.append(ParentNode(tag=f"h{level}", children=text_to_children(text)))
            
        elif block_type == "code":
            code_content = "\n".join(block.split("\n")[1:-1])
            block_nodes.append(ParentNode(tag="pre", children=[ParentNode(tag="code", children=text_to_children(code_content))]))
            
        elif block_type == "quote":
            text = "\n".join(line.lstrip('> ') for line in block.split("\n"))
            block_nodes.append(ParentNode(tag="blockquote", children=text_to_children(text)))
            
        elif block_type == "unordered_list":
            list_items = []
            for line in block.split("\n"):
                clean_line = re.sub(r"^[-*]\s+", "", line)  # Strip `-` or `*` followed by space, but keep the rest
                try:
                    list_items.append(ParentNode(tag="li", children=text_to_children(clean_line)))
                except ValueError as e:
                    print(f"Error processing list item: {line}")
                    raise e
            block_nodes.append(ParentNode(tag="ul", children=list_items))
            
        elif block_type == "ordered_list":
            list_items = []
            for line in block.split("\n"):
                clean_line = re.sub(r"^\d+\.\s+", "", line)  # Remove number + period + space
                try:
                    list_items.append(ParentNode(tag="li", children=text_to_children(clean_line)))
                except ValueError as e:
                    print(f"Error processing ordered list item: {line}")
                    raise e
            block_nodes.append(ParentNode(tag="ol", children=list_items))
            
        else:
            block_nodes.append(ParentNode(tag="p", children=text_to_children(block)))
            
    return ParentNode(tag="div", children=block_nodes)


def extract_title(markdown):
    for content in markdown:
        if content.startswith("#"):
            return content[1:].strip()
    raise ValueError("No title found in the markdown.")
