import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
       node = LeafNode("p", "Hello, world!")
       self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
   
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(),'<a href=https://www.google.com>Click me!</a>')

    def test_leaf_not_implemented(self):
       node = LeafNode("p", None)
       try:
           node.to_html()
       except ValueError as e:
        self.assertEqual(f'{e}', "LeafNode.to_html(): value must not be None")

if __name__ == "__main__":
    unittest.main(verbosity=2)

