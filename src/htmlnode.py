class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        temp = map(lambda x: f"{x}=\"{self.props[x]}\"", self.props)
        return " ".join(temp)

    def __repr__(self):
        return f"""HTMLNode({self.tag}, {self.value},
                            {self.children}, {self.props})"""

    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, props=props)
        self.value = value

    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.props == other.props)

    def to_html(self):
        chg_prop = ""
        if self.value is None:
            raise ValueError("Leaf node does not have value")
        if self.tag is not None:
            if self.props is None:
                return f'<{self.tag}>{self.value}</{self.tag}>'
            chg_prop += " " + self.props_to_html()
            return f'<{self.tag}{chg_prop}>{self.value}</{self.tag}>'
        return f'{self.value}'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, props=props)
        self.children = children

    def __eq__(self, other):
        return (self.tag == other.tag and
                self.children == other.children and
                self.props == other.props)

    def to_html(self):
        chg_prop = ""
        temp = []
        if self.tag is None:
            raise ValueError("no tag")
        if self.children == []:
            raise ValueError("no children")
        if self.props is not None:
            chg_prop += " " + self.props_to_html()
        for item in self.children:
            try:
                temp.append(item.to_html())
            except NotImplementedError as e:
                print(f"Failed to call to_html on {type(item)}: {e}")
        joined = "".join(temp)
        res = f"<{self.tag}{chg_prop}>{joined}</{self.tag}>"
        return res


def text_node_to_html_node(text_node):
    if text_node.text_type == "text":
        return LeafNode(value=text_node.text)
    if text_node.text_type == "bold":
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == "italic":
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == "code":
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == "link" and text_node.url is not None:
        return LeafNode(tag="a", value=text_node.text,
                        props={'href': text_node.url})
    if text_node.text_type == "image" and text_node.url is not None:
        return LeafNode(tag="img", props={'src': text_node.url,
                                          'alt': text_node.text})
    raise Exception(f"Text type not listed: {text_node.text_type}")











