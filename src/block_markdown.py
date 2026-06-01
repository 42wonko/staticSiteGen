# block_markdown.py
from enum import Enum
from contextlib import ContextDecorator
from sys import exception
from htmlnode import HTMLNode

import re

from inline_markdown import text_to_textnodes
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


def create_unordered_list(text):
    text_list = [x.rstrip() for x in text.split('-') if len(x) > 0]     # create a list of list-items removing \n
    node_list = [LeafNode('li', x) for x in text_list]                  # crate a list of proper HTML-nodes with <li> tags
    return node_list


def create_ordered_list(text):
    text_list = [x.rstrip() for x in text.split('\n') if len(x) > 0]
#    print(f"-D- ORDERED TEXT LIST: {text_list}")
    node_list = [LeafNode('li', x[len((re.match(r'^\d+\. ', x)).group()):]) for x in text_list]                  # crate a list of proper HTML-nodes with <li> tags
    return node_list


def markdown_to_html_node(markdown: str):
    node_list = []
    blocks: list[str] = markdown_to_blocks(markdown)
#    print(f"-D- markdown_to_html_node(): blocks={blocks}\n\n") 
#    print(f"-D- markdown_to_html_node(): num blocks={len(blocks)}\n\n")
    for block in blocks:
#        print(f"-D- new block: {block}")
        block_type = block_to_block_type(block)
#        print(f"-D: Type: {block_type}")
        match block_type:
            case BlockType.PARAGRAPH:
                node = ParentNode('p', text_to_children(block.replace('\n',' ')))
                node_list.append(node)
            case BlockType.HEADING:
                heading_tag = extract_heading(block)
                node = ParentNode(heading_tag, text_to_children(block.lstrip('#')))
                node_list.append(node)
            case BlockType.CODE:
                node = ParentNode('pre', [text_node_to_html_node(TextNode(block.strip('`').strip('\n'), TextType.CODE))])
                node_list.append(node)
            case BlockType.QUOTE:
                node = ParentNode('blockquote', text_to_children(block), None)
                node_list.append(node)
            case BlockType.UNORDERED_LIST:
                node = ParentNode('ul', create_unordered_list(block))
                node_list.append(node)
            case BlockType.ORDERED_LIST:
                node = ParentNode('ol', create_ordered_list(block))
                node_list.append(node)
            case _:
                pass
    return ParentNode('div', node_list, None)


