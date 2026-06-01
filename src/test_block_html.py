import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node 
from htmlnode import HTMLNode

class TestMarkdowToBlocks(unittest.TestCase):
    def test_html_mix(self):
        md = """
# this is the headline

This is **bolded** paragraph
text in a p
tag here

## new headline

This is another paragraph with _italic_ text and 

```
code
```

here

# a section containing an unordered list

- list item 1
- list item 2
- list item 3

## section containing orderes list

1. first item
2. second item
3. third item

### images

![image1](file:///home/micky/Pictures/14.jpg)
![image2](file:///home/micky/Pictures/0435.jpg)

###### links

[some link](https://127.0.0.1:8080)

The End
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
#        print(f"-D- HTML: {html}")
        self.assertEqual(html, '<div><h1> this is the headline</h1><p>This is <b>bolded</b> paragraph text in a p tag here</p><h2> new headline</h2><p>This is another paragraph with <i>italic</i> text and</p><pre><code>code</code></pre><p>here</p><h1> a section containing an unordered list</h1><ul><li> list item 1</li><li> list item 2</li><li> list item 3</li></ul><h2> section containing orderes list</h2><ol><li>first item</li><li>second item</li><li>third item</li></ol><h3> images</h3><p>![image1](file:///home/micky/Pictures/14.jpg) ![image2](file:///home/micky/Pictures/0435.jpg)</p><h6> links</h6><p><a href="https://127.0.0.1:8080">some link</a></p><p>The End</p></div>',)

    def test_html_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_html_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_html_unordered_list_01(self):
        md = """
- list item 1
- list item 2
- list item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li> list item 1</li><li> list item 2</li><li> list item 3</li></ul></div>"
        )

    def test_html_unordered_list_02(self):
        md = """
-list item 1
- list item 2
- list item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertNotEqual(
            html,
            "<div><ul><li> list item 1</li><li> list item 2</li><li> list item 3</li></ul></div>"
        )

    def test_html_unordered_list_01(self):
        md = """
- list item 1
- list item 2
- list item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li> list item 1</li><li> list item 2</li><li> list item 3</li></ul></div>"
        )

    def test_html_ordered_list_01(self):
        md = """
1. list item 1
2. list item 2
3. list item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>list item 1</li><li>list item 2</li><li>list item 3</li></ol></div>"
        )

    def test_html_ordered_list_02(self):
        md = """
0. list item 1
2. list item 2
3. list item 3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertNotEqual(
            html,
            "<div><ol><li>list item 1</li><li>list item 2</li><li>list item 3</li></ol></div>"
        )
        self.assertEqual(
            html,
            "<div><p>0. list item 1 2. list item 2 3. list item 3</p></div>"
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)

