import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.ITALIC , "https://www.heise.de")
        node2 = TextNode("This is a text node", TextType.ITALIC , "https://www.heise.de")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.LINK , "https://www.heise.de")
        node2 = TextNode("This is a text node", TextType.ITALIC , "https://www.heise.de")
        self.assertNotEqual(node, node2)

    def test_not_eq2(self):
        node = TextNode("This is a text node", TextType.ITALIC , "https://www,heise.de")
        node2 = TextNode("This is a text node", TextType.ITALIC , "https://www.heise.de")
        self.assertNotEqual(node, node2)

    def test_not_eq3(self):
        node = TextNode("This is a text node", TextType.ITALIC) 
        node2 = TextNode("This is a text node", TextType.ITALIC , "https://www.heise.de")
        self.assertNotEqual(node, node2)

    def test_not_eq4(self):
        node = TextNode("This is a text node", TextType.ITALIC) 
        node2 = TextNode("This is a text node", TextType.PLAIN)
        self.assertNotEqual(node, node2)

    def test_text_p(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_b(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold text node")
        self.assertEqual(html_node.to_html(), "<b>This is a bold text node</b>")

    def test_text_i(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "This is an italic text node")
        self.assertEqual(html_node.to_html(), "<i>This is an italic text node</i>")

    def test_text_code(self):
        node = TextNode("This is a code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "This is a code block")
        self.assertEqual(html_node.to_html(), "<code>This is a code block</code>")

    def test_text_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.to_html(), '<a href="https://www.google.com">This is a link</a>')

    def test_text_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.google.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), '<img src="https://www.google.com/image.jpg" alt="This is an image" />')



if __name__ == "__main__":
    unittest.main(verbosity=2)

