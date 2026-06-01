import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type

class TestMarkdowToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_1(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_2(self):
        md = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",


                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
 
    def test_blocktypes_unorder_list_1(self):
        block = """
- This is a list
- with items
"""
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_blocktypes_unorder_list_2(self):
        block = """
- This is a list
-with items
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.UNORDERED_LIST)

    def test_blocktypes_unorder_list_3(self):
        block = """
- This is a list
- with items
invalid item
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.UNORDERED_LIST)

    def test_blocktypes_Order_list_1(self):
        block = """
1. This is a list item 1
2. this is item 2
"""
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_blocktypes_Order_list_2(self):
        block = """
2. This is a list item 1
3. this is item 2
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_blocktypes_Order_list_3(self):
        block = """
1. This is a list item 1
3. this is item 2
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_blocktypes_Order_list_4(self):
        block = """
1. This is a list item 1
2.this is item 2
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)

    def test_blocktypes_Order_list_5(self):
        block = """
1. This is a list item 1
2. this is item 2
invalis
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.ORDERED_LIST)



    def test_blocktypes_quote_1(self):
        block = """
> This is a qute
>this is a second qote
"""
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_blocktypes_quote_2(self):
        block = """
> This is a qute
> this is a second qote
"""
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_blocktypes_quote_3(self):
        block = """
> This is a qute
> this is a second qote
invalid
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.QUOTE)

    def test_blocktypes_code_1(self):
        block = """
```
This is a code block
 line 1
 line 2
```
"""
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.CODE)

    def test_blocktypes_code_2(self):
        block = """
````
This is a code block
 line 1
 line 2
```
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_blocktypes_code_3(self):
        block = """
```
This is a code block
 line 1
 line 2
````
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_blocktypes_code_4(self):
        block = """
``` This is a code block
 line 1
 line 2
```
"""
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.CODE)

    def test_blocktypes_heading_1(self):
        block = "#heading 1"
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.HEADING)

    def test_blocktypes_heading_2(self):
        block = "# heading 2"
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.HEADING)

    def test_blocktypes_heading_3(self):
        block = "## heading 2"
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.HEADING)

    def test_blocktypes_heading_4(self):
        block = "### heading 2"
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.HEADING)

    def test_blocktypes_heading_5(self):
        block = "#### heading 2"
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.HEADING)

    def test_blocktypes_heading_6(self):
        block = "##### heading 2"
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.HEADING)

    def test_blocktypes_heading_7(self):
        block = "###### heading 2"
        block_type = block_to_block_type(block.strip())
        self.assertEqual(block_type, BlockType.HEADING)

    def test_blocktypes_heading_8(self):
        block = "####### heading 2"
        block_type = block_to_block_type(block.strip())
        self.assertNotEqual(block_type, BlockType.HEADING)


if __name__ == "__main__":
    unittest.main(verbosity=2)

