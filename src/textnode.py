import re


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url)

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def __nonzero__(self):
        return bool(self.text or self.text_type or self.url)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        temp_list = []
        if isinstance(node, TextNode) is False:
            res.append(node)
        if checker_of_dem(delimiter, node.text) is False:
            raise Exception("Invalid Markdown Syntax " +
                            "there are only " +
                            f"{len(node.text.split(delimiter))-1}" +
                            " delimeters")
        split = node.text.split(delimiter)
        for i in range(len(split)):
            if i == 0 or i % 2 == 0:
                temp_list.append(TextNode(split[i], node.text_type))
            else:
                temp_list.append(TextNode(split[i], text_type))
        res.extend(temp_list)
    return res


def checker_of_dem(dem, text):
    count = 0
    for i in range(len(text)):
        if text[i:i+len(dem)] == dem:
            count += 1
    return count % 2 == 0


def extract_markdown_images(text):
    temp_tup = []
    temp = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    for item in temp:
        temp_tup.append(item)
    return temp_tup


def extract_markdown_links(text):
    temp_tup = []
    temp = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    for item in temp:
        temp_tup.append(item)
    return temp_tup


def split_nodes_image(old_nodes):
    temp = []
    for node in old_nodes:
        if node:
            if extract_markdown_images(node.text) == []:
                temp.append(node)
            else:
                new_txt = node.text
                record = extract_markdown_images(node.text)
                for i in range(len(record)):
                    a = trap_image(new_txt, node.text_type, record[i])
                    if i < len(record)-1:
                        temp.extend(a[0:len(a)-1])
                        new_txt = a[len(a)-1].text
                    else:
                        temp.extend(a)
    return temp


def trap_image(text, type, tup):
    markdown = f"![{tup[0]}]({tup[1]})"
    split = text.split(markdown)
    return eliminate_empty_node([TextNode(split[0], type),
                                 TextNode(tup[0], "image", tup[1]),
                                 TextNode(split[1], type)])


def split_nodes_link(old_nodes):
    temp = []
    for node in old_nodes:
        if node:
            if extract_markdown_links(node.text) == []:
                temp.append(node)
            else:
                new_txt = node.text
                record = extract_markdown_links(node.text)
                for i in range(len(record)):
                    a = trap_link(new_txt, node.text_type, record[i])
                    if i < len(record)-1:
                        temp.extend(a[0:len(a)-1])
                        new_txt = a[len(a)-1].text
                    else:
                        temp.extend(a)
    return temp


def trap_link(text, type, tup):
    markdown = f"[{tup[0]}]({tup[1]})"
    split = text.split(markdown)
    return eliminate_empty_node([TextNode(split[0], type),
                                 TextNode(tup[0], "link", tup[1]),
                                 TextNode(split[1], type)])


def eliminate_empty_node(list):
    replacement = []
    for item in list:
        if item.text != '':
            replacement.append(item)
    return replacement




