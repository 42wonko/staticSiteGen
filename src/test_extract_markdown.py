import unittest

from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, text_to_textnodes

class TestSplitNodeDelimiter(unittest.TestCase):
    # test for extact markdown images
    def test_extract_markdown_images_1(self):
        matches = extract_markdown_images( "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_2(self):
        matches = extract_markdown_images( "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    # test for extract markdown links
    def test_extract_markdown_links_1(self):
        matches = extract_markdown_links( "This is text with an [link](https://i.imgur.com)")
        self.assertListEqual([("link", "https://i.imgur.com")], matches)

    def test_extract_markdown_links_2(self):
        matches = extract_markdown_links( "This is text with an [link](https://i.imgur.com) and again[obi wan](https://i.imgur.com/fJRm4Vk)")
        self.assertListEqual([("link", "https://i.imgur.com"), ("obi wan", "https://i.imgur.com/fJRm4Vk")], matches)
    
    #tests for turning text into nodes
    def test_text_2_node_1(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], nodes
        )
if __name__ == "__main__":
    unittest.main(verbosity=2)

