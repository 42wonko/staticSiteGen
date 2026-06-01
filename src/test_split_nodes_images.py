import unittest
from inline_markdown import split_nodes_delimiter, split_nodes_image
from textnode import TextNode, TextType


class TestSplitNodeDelimiter(unittest.TestCase):
    def test_split_Image_1(self):
        node = TextNode("This is text with an ![alt image text](https://127.0.0.1/srv/root/image1.png) image and a second one .![very alt image](https://localhost/home/user/Pictures/image2.jpeg)", TextType.PLAIN, )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.PLAIN),
            TextNode("alt image text", TextType.IMAGE, "https://127.0.0.1/srv/root/image1.png"),
            TextNode(" image and a second one .", TextType.PLAIN),
            TextNode("very alt image", TextType.IMAGE, "https://localhost/home/user/Pictures/image2.jpeg"
            ),
        ],
        new_nodes,
    )

    def test_split_image_2(self):
        node = TextNode("![alt image](https://127.0.0.1/srv/root/image1.png) Just an image and a second one .![very alt image](https://localhost/home/user/Pictures/image2.jpeg)", TextType.PLAIN, )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("alt image", TextType.IMAGE, "https://127.0.0.1/srv/root/image1.png"),
            TextNode(" Just an image and a second one .", TextType.PLAIN),
            TextNode("very alt image", TextType.IMAGE, "https://localhost/home/user/Pictures/image2.jpeg"
            ),
        ],
        new_nodes,
    )

if __name__ == "__main__":
    unittest.main(verbosity=2)

