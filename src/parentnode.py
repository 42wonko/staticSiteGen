# defines class ParentNode
from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Method ParentNode.to_html() tag must not be None")
        if self.children == None:
            raise ValueError("Method ParentNode.to_html() children must not be None")

        s = f'<{self.tag}{self.props_to_html() if self.props else ""}>'
        for c in self.children:
            s += c.to_html()
        s += f'</{self.tag}>'
        return s
