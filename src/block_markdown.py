import re

def markdown_to_blocks(markdown):
    blocks = re.split(r'\n\s*\n+', markdown)
    list_blocks = [block.strip() for block in blocks if block.strip()]
    return list_blocks
    
def block_to_block_type(block):
    lines = block.split("\n")
    first_line = lines[0].strip() if lines else ""

    if first_line.startswith("#"):
        if re.match(r'^#{1,6} ', first_line):
            return "heading"

    if first_line.startswith("```") and block.endswith("```"):
        return "code"

    if all(line.strip().startswith(">") for line in lines):
        return "quote"

    if all(re.match(r'^(\*|-)\s+', line.strip()) for line in lines):
        return "unordered_list"

    if all(re.match(r'^\d+\.\s+', line.strip()) for line in lines):
        return "ordered_list"

    return "paragraph"
