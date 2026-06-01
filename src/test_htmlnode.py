import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("Tag1", "12", None, {"href":"https://www.google.com", "target":"_blank"})
        node2 = HTMLNode("Tag2", None, [node1], None)
        self.assertEqual(f'{node2}', "tag=Tag2, value:None,\ntag=Tag1, value:12, href=https://www.google.com target=_blank")

    def test_eq2(self):
        node1 = HTMLNode("Tag1", "12", None, {"href":"https://heise.de", "target":"_blank"})
        self.assertEqual(node1.props_to_html(), " href=https://heise.de target=_blank")

    def test_children(self):
        node1 = HTMLNode("Tag1", "1", None, None)
        node2 = HTMLNode("Tag2", "2", None, None)
        node3 = HTMLNode("Tag3", "3", None, None)
        node4 = HTMLNode("Tag4", "4", [node1, node2, node3], None)
        self.assertEqual(f'{node4}', "tag=Tag4, value:4,\ntag=Tag1, value:1,\ntag=Tag2, value:2,\ntag=Tag3, value:3,")

    def test_not_implemented(self):
        node = HTMLNode("Tag1", "12", None, {"href":"https://www.google.com", "target":"_blank"})
        try:
            node.to_html()
        except NotImplementedError as e:
            self.assertEqual(f'{e}', "Method HTMLNode.to_html() is not implemented")



if __name__ == "__main__":
    unittest.main(verbosity=2)

