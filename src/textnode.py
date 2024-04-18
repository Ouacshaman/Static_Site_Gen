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


def split_nodes_images(old_nodes):
    temp = []
    for node in old_nodes:
        if node:
            if re.findall(r"!\[(.*?)\]\((.*?)\)", node.text) == []:
                temp.append(node)
            record = extract_markdown_images(node.text)
            new_txt = node.text
            magic = trap(new_txt, record, r"!\[(.*?)\]\((.*?)\)")
            res = transfer(magic,
                           node.text_type,
                           "image", r"!\[(.*?)\]\((.*?)\)")
            temp.extend(res)
        else:
            pass
    return temp


def split_nodes_link(old_nodes):
    temp = []
    for node in old_nodes:
        if node:
            if re.findall(r"\[(.*?)\]\((.*?)\)", node.text) == []:
                temp.append(node)
            record = extract_markdown_links(node.text)
            new_txt = node.text
            magic = trap(new_txt, record, r"\[(.*?)\]\((.*?)\)")
            res = transfer(magic,
                           node.text_type,
                           "link", r"\[(.*?)\]\((.*?)\)")
            temp.extend(res)
        else:
            pass
    return temp


def trap(text, record, pattern):
    new_txt = text
    rec = []
    new_rec = []
    tup_rec = []
    single = ""
    if pattern == r"!\[(.*?)\]\((.*?)\)":
        single = "!"
    if pattern == r"\[(.*?)\]\((.*?)\)":
        single = ""
    for tup in record:
        tup_rec.append(f"{single}[{tup[0]}]({tup[1]})")
        ref = new_txt.split(f"{single}[{tup[0]}]({tup[1]})", 1)
        for item in ref:
            if re.findall(pattern, item) == []:
                rec.append(item)
        new_txt = "".join(ref)
    for i in range(len(rec)):
        new_rec.append(rec[i][len(rec[i-1]):])
    new_list = tup_rec
    new_list.extend(new_rec)
    tuple_list = []
    for item in new_list:
        tuple_list.append((item, text.index(item)))
    sorted_list = sorted(tuple_list, key=lambda x: x[1])
    no_empty = []
    for item in sorted_list:
        if item[0] != '':
            no_empty.append(item)
    return no_empty



def transfer(lst, old, new, pttr):
    new_lst = []
    for item in lst:
        if re.findall(pttr, item[0]) == []:
            new_lst.append(TextNode(item[0], old))
        else:
            re_run = re.findall(pttr, item[0])
            new_lst.append(TextNode(re_run[0][0], new, re_run[0][1]))
    return new_lst

















