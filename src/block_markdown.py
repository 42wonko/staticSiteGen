# block_markdown.py
from enum import Enum
from contextlib import ContextDecorator
from sys import exception
from htmlnode import HTMLNode

import re

from inline_markdown import text_to_textnodes, split_nodes_link

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH       = "paragraph"
    HEADING         = "heading"
    CODE            = "code"
    QUOTE           = "quote"
    UNORDERED_LIST  = "unordered_list"
    ORDERED_LIST    = "ordered_list"
    

def markdown_to_blocks(markdown):
    return [item.strip() for item in markdown.split('\n\n') if item.strip()]


def is_ordered_list(text):
    lines = text.strip().split('\n')            # split into single lines
    pattern = re.compile(r'^\d+\. .*$')         # ine staring with a number, followed by a '.' and a ' '. then text

    for i, line in enumerate(lines, start=1):   # index the lines staarting at !
        if not pattern.fullmatch(line):         # if the line is not a number followed by a '. ' and then some text, the list is not ordered
            return False
        number = int(line.split('.')[0])        # if the line is valid, check if the numbering is incrementing by one
        if number != i:
            return False

    return True

def block_to_block_type(block):
    if bool(re.match(r"^(#{1,6}) \w*", block)):
        return BlockType.HEADING
    elif bool(re.match(r"^`{3}\n(.|\s)*\n`{3}$", block)):
        return BlockType.CODE
    elif bool(re.match(r"^(?:> ?.*(?:\n|$))+$", block)):
        return BlockType.QUOTE
    elif bool(re.match(r"^(?:- .*(?:\n|$))+$", block)):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH 


def text_to_children(text):
    result_list = []
    node_list = text_to_textnodes(text)
    result_list = [(lambda x: text_node_to_html_node(x))(x) for x in node_list]
    return result_list


def extract_heading(text):
    heading = 0
    myMatch = re.match(r"^(#{1,6}) ", text)
    if myMatch != None:
        heading = len(myMatch.group().rstrip())
    else:
        raise SyntaxError(f"Error: Invalid heading! <{text[:10]}...>")

    return f'h{heading}'

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.PLAIN)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

