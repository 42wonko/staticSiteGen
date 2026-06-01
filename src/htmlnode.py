# defines calss HTMLNode

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag        = tag       # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value      = value     # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children   = children  # A list of HTMLNode objects representing the children of this node
        self.props      = props     # A dictionary of key-value pairs representing the attributes of the HTML tag

    def to_html(self):
        raise NotImplementedError("Method HTMLNode.to_html() is not implemented")

    def props_to_html(self):
        result_str = ""
        if self.props:
            for key, value in self.props.items():
                result_str += f' {key}={value}'

        return result_str

    def __repr__(self):
        s = f'tag={self.tag}, value:{self.value},'
        if self.children:
            for c in self.children:
                s += f'\n{c}'
        s += self.props_to_html()
        return s
