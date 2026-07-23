# inline_markdown.py

import re
from typing import Text
from textnode import TextNode, TextType

def extract_markdown_images(text):
    return re.findall(r"!\[([\w*\s*]*)\]\(([\w*\s*.\/]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[([^\[\]]*)\]\(([^\[\]]*)\)", text)


def extract_title(markdown):
    text = re.match(r"^# [a-zA-Z0-9 ]+", markdown)
    if None == text:
        raise LookupError("No h1-header found!")
    return text[0].lstrip('#').lstrip(' ')


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result_lst = []
    process_text = True                     # flag indication wheter current string is text-block or a special-block

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result_lst.append(node)
        else:
            if node.text.count(delimiter)%2 != 0:           # check if delimiter has an even number of occurrences
                raise SyntaxError(f"Error: <{node.text}> is not valid markdown syntax")
            text_lst = list(filter(lambda x:len(x)>0, node.text.split(delimiter)))
            if node.text[0:len(delimiter)] == delimiter:    # the first node in the list is a special node
                process_text = False
            else:
                process_text = True
            t = text_lst.pop(0)
            while t != None:
                if process_text:            # current string should become a text node
                    result_lst.append(TextNode(t,TextType.PLAIN,None))
                    process_text = False
                else:                       # current string should be a node of type text_type
                    result_lst.append(TextNode(t,text_type,None))
                    process_text = True
                if text_lst:
                    t = text_lst.pop(0)
                else:
                    break

    return result_lst

def split_nodes_link(old_nodes):
    result_lst = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result_lst.append(node)
        else:
            text_orig = node.text
            link_list = extract_markdown_links(text_orig)
            if not link_list:
                result_lst.append(node)
            for link in link_list:
                link_delim = f'[{link[0]}]({link[1]})'
                text_lst = text_orig.split(link_delim, 1)
                if(node.text.find(link_delim) != 0):
                    result_lst.append(TextNode(text_lst[0],TextType.PLAIN))
                    result_lst.append(TextNode(link[0],TextType.LINK,link[1]))
                    text_lst.pop(0)
                else:
                    result_lst.append(TextNode(link[0],TextType.LINK,link[1]))
                    text_lst.pop(0)                     # first element is processed
                if text_lst:
                    text_orig = text_lst.pop(0)         # get ready for splittinng the rest

    return result_lst

def split_nodes_image(old_nodes):
    result_lst = []
    text_lst = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            result_lst.append(node)
        else:
            text_orig = node.text
            image_list = extract_markdown_images(text_orig)
            if not image_list:
                result_lst.append(node)
                text_orig = ''
            for image in image_list:
                link_delim = f'![{image[0]}]({image[1]})'
                text_lst = text_orig.split(link_delim, 1)
                txt = text_lst.pop(0)
                if(node.text.find(link_delim) != 0):
                    result_lst.append(TextNode(txt,TextType.PLAIN))
                    result_lst.append(TextNode(image[0], TextType.IMAGE, image[1]))
                else:
                    result_lst.append(TextNode(image[0], TextType.IMAGE, image[1]))
                if text_lst:
                    text_orig = text_lst.pop(0)         # get ready for splittinng the rest
            if text_orig:
                result_lst.append(TextNode(text_orig,TextType.PLAIN))

    return result_lst

def text_to_textnodes(text):
    result_lst = []
    result_lst=split_nodes_delimiter([TextNode(text, TextType.PLAIN,)], '**', TextType.BOLD)
    result_lst=split_nodes_delimiter(result_lst, '_', TextType.ITALIC)
    result_lst=split_nodes_delimiter(result_lst, '`', TextType.CODE)
    result_lst=split_nodes_link(result_lst)
    result_lst=split_nodes_image(result_lst)
    return result_lst

