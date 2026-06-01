# inline_markdown.py

import re
from typing import Text
from textnode import TextNode, TextType

def extract_markdown_images(text):
#    return re.findall(r"\[(.*?)\]\((https://\w+\.\w+\.\w+/\w+\.\w+)\)", text)
    return re.findall(r"!\[(.*?)\]\((https:\/\/[^\s]*\/[^\s]+)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((https://[^\s)]+)\)", text)

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
#            print(f'-D- node-text:{node.text}')
#            print(f'-D- text_lst:{text_lst}')
            if node.text[0:len(delimiter)] == delimiter:    # the first node in the list is a special node
#                print(f'-D- node starts with delimiter:{delimiter}')
                process_text = False
            else:
#                print('-D- node starts with text')
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
#            print(f'-D- text_orig:{text_orig}')
#            print(f'-D- extracted links:{link_list}')
            if not link_list:
#                print('-D- no links found -> appending')
                result_lst.append(node)
            for link in link_list:
                link_delim = f'[{link[0]}]({link[1]})'
#                print(f'-D- splitting "{text_orig}" at {link_delim}')
                text_lst = text_orig.split(link_delim, 1)
#                print(f'-D- split text:{text_lst}')
#                print(f'-D- links:{link_list}')
#                print(f'-D- curr link:{link}')
                if(node.text.find(link_delim) != 0):
#                    print(f'-D- textnode starts with text')
                    result_lst.append(TextNode(text_lst[0],TextType.PLAIN))
                    result_lst.append(TextNode(link[0],TextType.LINK,link[1]))
                    text_lst.pop(0)
                else:
#                    print(f'-D- textnode starts link')
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
#            print(f'-D- text_orig:{text_orig}')
#            print(f'-D- extracted links:{image_list}')
            if not image_list:
#                print('-D- no images found -> appending')
                result_lst.append(node)
                text_orig = ''
            for image in image_list:
                link_delim = f'![{image[0]}]({image[1]})'
#                print(f'-D- splitting "{text_orig}" at {link_delim}')
                text_lst = text_orig.split(link_delim, 1)
                txt = text_lst.pop(0)
#                print(f'-D- split text:{text_lst}')
#                print(f'-D- images:{image_list}')
#                print(f'-D- curr image:{image}')
                if(node.text.find(link_delim) != 0):
#                    print(f'-D- textnode starts with text')
                    result_lst.append(TextNode(txt,TextType.PLAIN))
                    result_lst.append(TextNode(image[0], TextType.IMAGE, image[1]))
#                    text_lst.pop(0)                     # first element is processed
                else:
#                    print(f'-D- textnode starts image')
                    result_lst.append(TextNode(image[0], TextType.IMAGE, image[1]))
#                    text_lst.pop(0)                     # first element is processed
                if text_lst:
#                    print(f'-D- FOUND: text_lst:{text_lst}')
                    text_orig = text_lst.pop(0)         # get ready for splittinng the rest
            if text_orig:
                result_lst.append(TextNode(text_orig,TextType.PLAIN))

    return result_lst

def text_to_textnodes(text):
    result_lst = []
    result_lst=split_nodes_delimiter([TextNode(text, TextType.PLAIN,)], '**', TextType.BOLD)
#    print(f'-D- result_list after bold: {result_lst}')
    result_lst=split_nodes_delimiter(result_lst, '_', TextType.ITALIC)
#    print(f'-D- result_listafter italic: {result_lst}')
    result_lst=split_nodes_delimiter(result_lst, '`', TextType.CODE)
#    print(f'-D- result_list after code: {result_lst}')
    result_lst=split_nodes_link(result_lst)
#    print(f'-D- result_list after link: {result_lst}')
    result_lst=split_nodes_image(result_lst)
#    print(f'-D- result_list after image: {result_lst}')
    return result_lst

