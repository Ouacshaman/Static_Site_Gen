import re
from htmlnode import HTMLNode, ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code block"
block_type_quote = "quote"
block_type_ul = "unordered list"
block_type_ol = "ordered list"


def markdown_to_blocks(markdown):
    block_lst = []
    for item in markdown.split("\n\n"):
        if item != "":
            block_lst.append(item)
    lead_strip = map(lambda x: x.strip(), block_lst)
    res = list(filter(lambda x: x != "", lead_strip))
    return res


def block_to_block_type(markdown):
    if is_header(markdown):
        return block_type_heading
    if is_code(markdown):
        return block_type_code
    if is_quote(markdown):
        return block_type_quote
    if is_ul(markdown):
        return block_type_ul
    if is_ol(markdown):
        return block_type_ol
    return block_type_paragraph


def is_header(text):
    if re.match(r"#{1,6}\s+.*", text):
        return True
    return False


def is_code(text):
    if (re.match(r"`{3}", text) and
            re.search(r".*`{3}$", text)):
        return True
    return False


def is_quote(text):
    return all(re.match(r"^>.*", line) for line in text.split("\n"))


def is_ul(text):
    return all(re.match(r"\s*[*-]\s.*", line) for line in text.split("\n"))


def is_ol(text):
    split_up = text.split("\n")
    for i in range(len(split_up)):
        if f"{i+1}. " in split_up[i]:
            pass
        else:
            return False
    return True


def markdown_to_html_node(markdown):
    check_pt_01 = markdown_to_blocks(markdown)
    if check_pt_01 == [] or markdown == "":
        return ParentNode("div", [])
    res = []
    for item in check_pt_01:
        if block_to_block_type(item) == block_type_quote:
            res.extend(quote_to_html(item))
        elif block_to_block_type(item) == block_type_ul:
            res.append(ul_to_html(item))
        elif block_to_block_type(item) == block_type_ol:
            res.append(ol_to_html(item))
        elif block_to_block_type(item) == block_type_code:
            res.append(code_to_html(item))
        elif block_to_block_type(item) == block_type_heading:
            res.append(hd_to_html(item))
        else:
            res.append(p_to_html(item))
    return ParentNode("div", res)


def quote_to_html(txt):
    chk_pt = re.findall(r">.*", txt)
    res = []
    for item in chk_pt:
        res.append(HTMLNode("blockquote", item.strip(">")))
    return res


def ul_to_html(txt):
    chk_pt = re.findall(r"\s*[*-]\s.*", txt)
    res = []
    for item in chk_pt:
        res.append(HTMLNode("li", re.sub(r"^\s*[-,*]\s", "", item).strip()))
    return ParentNode("ul", res)


def ol_to_html(txt):
    chk_pt = re.findall(r"[0-9]*\.\s.*", txt)
    res = []
    for item in chk_pt:
        res.append(HTMLNode("li", re.sub(r"^[0-9]*\.\s", "", item).strip()))
    return ParentNode("ol", res)


def code_to_html(txt):
    chk_pt = txt.strip("`")
    res = HTMLNode("code", chk_pt)
    return ParentNode("pre", [res])


def hd_to_html(txt):
    header_ct = 0
    for char in txt:
        if char == "#":
            header_ct += 1
        else:
            break
    if re.match(r"^#{1,6}\s+.*", txt):
        return HTMLNode(f"h{header_ct}", txt.lstrip("#").strip())
    return p_to_html(txt)


def p_to_html(txt):
    return HTMLNode("p", txt)


case_01 = """> a
> b"""
quote_to_html(case_01)
print(quote_to_html(case_01))

case_02 = """1. grap2. es
2. app1. le
3. end"""

print(ol_to_html(case_02))

case_03 = """```I await the holy grail
none can fathom my desire's for enternity```"""

print(code_to_html(case_03))

case_04 = "#a## jaba the hut"

case_05 = """- dragon ball
 - take*n away"""

case_06 = """drunken fist is fun to watch
but I want to eat food"""

print(markdown_to_html_node(case_01))
print(markdown_to_html_node(case_02))
print(markdown_to_html_node(case_03))

list_of_block = [case_01, case_02, case_03, case_04, case_05, case_06]
joined_block = "\n\n".join(list_of_block)
print(joined_block)

print(markdown_to_html_node(joined_block))








