import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_syntax_error(self):
        node = TextNode("This is text with a `code block` `word", TextType.PLAIN)
        with self.assertRaises(SyntaxError): result=split_nodes_delimiter([node], "`", TextType.CODE)

    def test_code_1(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertEqual(node_types, (TextType.PLAIN, TextType.CODE, TextType.PLAIN) )

    # two consecutive code blocks without space inbetween is not allowd
    def test_code_2(self):
        node = TextNode("This is text with `code block 1``code block 2` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertNotEqual(node_types, (TextType.PLAIN, TextType.CODE, TextType.CODE, TextType.PLAIN) )

    def test_code_3(self):
        node = TextNode("`code block 0` This is text with `code block 1` `code block 2` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertEqual(node_types, (TextType.CODE, TextType.PLAIN, TextType.CODE, TextType.PLAIN, TextType.CODE, TextType.PLAIN) )

    def test_syntax_error_bold(self):
        node = TextNode("This is text with a **bold test** **word", TextType.PLAIN)
        with self.assertRaises(SyntaxError): result=split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_bold_1(self):
        node = TextNode("**bold block 0** This is text with **bold block 1** **bold block 3** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertEqual(node_types, (TextType.BOLD, TextType.PLAIN, TextType.BOLD, TextType.PLAIN, TextType.BOLD, TextType.PLAIN) )

    def test_bold_2(self):
        node = TextNode("This is text with a **bold block** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertEqual(node_types, (TextType.PLAIN, TextType.BOLD, TextType.PLAIN) )

    # two consecutive bold blocks without space inbetween is not allowd
    def test_bold_3(self):
        node = TextNode("This is text with **bold block 1****bold block 2** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertNotEqual(node_types, (TextType.PLAIN, TextType.BOLD, TextType.BOLD, TextType.PLAIN) )

    def test_bold_4(self):
        node = TextNode("This is text with **bold block 1** **bold block 2** word", TextType.PLAIN)
        node2 = TextNode("bold block 0", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node2, node], "**", TextType.BOLD)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertEqual(node_types, (TextType.BOLD, TextType.PLAIN, TextType.BOLD, TextType.PLAIN, TextType.BOLD, TextType.PLAIN) )


    def test_syntax_error_italic(self):
        node = TextNode("This is text with a _italic test_ _word", TextType.PLAIN)
        with self.assertRaises(SyntaxError): result=split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_italic_1(self):
        node = TextNode("_italic block 0_ This is text with _italic block 1_ _italic block 3_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertEqual(node_types, (TextType.ITALIC, TextType.PLAIN, TextType.ITALIC, TextType.PLAIN, TextType.ITALIC, TextType.PLAIN) )

    def test_italic_2(self):
        node = TextNode("This is text with a _italic block_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertEqual(node_types, (TextType.PLAIN, TextType.ITALIC, TextType.PLAIN) )

    # two consecutive italic blocks without space inbetween is not allowd
    def test_italic_3(self):
        node = TextNode("This is text with _italic block 1__italic block 2_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
        self.assertNotEqual(node_types, (TextType.PLAIN, TextType.ITALIC, TextType.ITALIC, TextType.PLAIN) )

    def test_italic_4(self):
        node = TextNode("This is text with _italic block 1_ _italic block 2_ word", TextType.PLAIN)
        node2 = TextNode("italic block 0", TextType.ITALIC)
        new_nodes = split_nodes_delimiter([node2, node], "_", TextType.ITALIC)
        node_types = ()
        for i in range(len(new_nodes)):
            node_types += (new_nodes[i].text_type,)
  #      self.assertEqual(node_types, (TextType.ITALIC, TextType.PLAIN, TextType.ITALIC, TextType.PLAIN, TextType.ITALIC, TextType.PLAIN) )
        self.assertListEqual(
            [
                TextNode("italic block 0", TextType.ITALIC),
                TextNode("This is text with ", TextType.PLAIN),
                TextNode("italic block 1", TextType.ITALIC),
                TextNode(" ", TextType.PLAIN),
                TextNode("italic block 2",TextType.ITALIC),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes
        )
    
    def test_italic_code_1(self):
        node = TextNode("This is text with _italic block 1_ and `a code block` text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.PLAIN),
                TextNode("italic block 1", TextType.ITALIC),
                TextNode(" and `a code block` text", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_italic_code_2(self):
        node = TextNode("This is text with `a code block` and _italic_ text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with `a code block` and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_italic_code_3(self):
        node = TextNode("This is text with _italic block 1_ and `a code block` text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with _italic block 1_ and ", TextType.PLAIN),
                TextNode("a code block", TextType.CODE),
                TextNode(" text", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_italic_code_4(self):
        node = TextNode("This is text with `a code block` and _italic_ text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.PLAIN),
                TextNode("a code block", TextType.CODE),
                TextNode(" and _italic_ text", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_italic_code_5(self):
        node = TextNode("_italic block 1_ starts a the beginning and `a code block` text", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("italic block 1", TextType.ITALIC),
                TextNode(" starts a the beginning and `a code block` text", TextType.PLAIN),
            ],
            new_nodes
        )


    def test_italic_bold_1(self):
        node = TextNode("This is text with _italic block 1_ and **bold** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.PLAIN),
                TextNode("italic block 1", TextType.ITALIC),
                TextNode(" and **bold** word", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_italic_bold_2(self):
        node = TextNode("This is text with **bold** and _italic_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with **bold** and ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.PLAIN),
            ],
            new_nodes
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)

