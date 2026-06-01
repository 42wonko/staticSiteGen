import unittest

from inline_markdown import split_nodes_delimiter, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_link_1(self):
        node = TextNode("This is text with a [alt text](https://127.0.0.1:8080) link and a second one .[very alt text](https://localhost:8080)", TextType.PLAIN, )
        new_nodes = split_nodes_link([node])
#        print(f'-T- {new_nodes}')
        self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("alt text", TextType.LINK, "https://127.0.0.1:8080"),
            TextNode(" link and a second one .", TextType.PLAIN),
            TextNode("very alt text", TextType.LINK, "https://localhost:8080"
            ),
        ],
        new_nodes,
    )

    def test_split_link_2(self):
        node = TextNode("[alt text](https://127.0.0.1:8080) Just a link and a second one .[very alt text](https://localhost:8080)", TextType.PLAIN, )
        new_nodes = split_nodes_link([node])
#        print(f'-T- {new_nodes}')
        self.assertListEqual(
        [
            TextNode("alt text", TextType.LINK, "https://127.0.0.1:8080"),
            TextNode(" Just a link and a second one .", TextType.PLAIN),
            TextNode("very alt text", TextType.LINK, "https://localhost:8080"
            ),
        ],
        new_nodes,
    )


if __name__ == "__main__":
    unittest.main(verbosity=2)

