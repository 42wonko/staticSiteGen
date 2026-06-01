# defines calss HTMLNode
from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("LeafNode.to_html(): value must not be None")
        if self.tag == None:
            return f'{self.value}'
        if self.tag == 'img':
            return f'<{self.tag}{self.props_to_html()} />'
        else:
            return f'<{self.tag}{self.props_to_html() if self.props else ""}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f'tag={self.tag}, value:{self.value}, {self.props_to_html()}'

