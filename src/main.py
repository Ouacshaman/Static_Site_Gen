from textnode import TextNode
import os
import shutil
from blocknode import (markdown_to_blocks,
                       markdown_to_html_node,
                       block_to_block_type)
from pathlib import Path


def main():
    Init_node = TextNode("drunken fist", "bold", "www.google.com")
    print(Init_node)
    from_p = "/Users/shihong/Downloads/Code/Create/proj04/Static_Site_Gen/content/"
    from_tmplt = "/Users/shihong/Downloads/Code/Create/proj04/Static_Site_Gen/template.html"
    dest_p = "/Users/shihong/Downloads/Code/Create/proj04/Static_Site_Gen/public/"
    #  generate_page(from_p, from_tmplt, dest_p)
    generate_pages_recursive(from_p, from_tmplt, dest_p)


def copy_static(input, target):
    dir_lst = os.listdir(target)
    if dir_lst != []:
        for item in dir_lst:
            if os.path.isfile(os.path.join(target, item)) is False:
                try:
                    shutil.rmtree(os.path.join(target, item))
                except (PermissionError, FileNotFoundError) as e:
                    print(e)
            else:
                try:
                    os.remove(os.path.join(target, item))
                except (FileNotFoundError, PermissionError) as e:
                    print(e)
    final_copy_over(input, target)


def final_copy_over(input_dir, target_dir):
    if not os.path.exists(input_dir) or not os.path.exists(target_dir):
        raise FileNotFoundError("file does not exist")
    dir_list = os.listdir(input_dir)
    for item in dir_list:
        if os.path.isfile(os.path.join(input_dir, item)):
            try:
                shutil.copy(os.path.join(input_dir, item), target_dir)
            except (FileExistsError, PermissionError, IOError) as e:
                print(e)
        else:
            moved = os.path.join(target_dir, item)
            try:
                os.mkdir(moved)
            except FileExistsError as e:
                print(e)
            final_copy_over(os.path.join(input_dir, item), moved)


def extract_title(markdown):
    block = markdown_to_blocks(markdown)
    for item in block:
        if block_to_block_type(item) == "heading":
            if "# " in item:
                return item.strip("#").strip()
    raise Exception("no h1 headings")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path}" +
          f" to {dest_path} using {template_path}")
    open_from = open(from_path, "r")
    rd_from = open_from.read()
    open_templt = open(template_path, "r")
    rd_temp = open_templt.read()
    md_html_node = markdown_to_html_node(rd_from)
    converted_md = md_html_node.to_html()
    ex_title = extract_title(rd_from)
    replace_title = rd_temp.replace("{{ Title }}", ex_title)
    replace_content = replace_title.replace("{{ Content }}", converted_md)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=False)
        open_new = open(dest_path, "x")
        open_new.write(replace_content)
        open_new.close()
    else:
        open_dest = open(dest_path, "w")
        open_dest.write(replace_content)
    open_dest.close()
    open_from.close()
    open_templt.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    copy_static(dir_path_content, dest_dir_path)
    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        if (os.path.isfile(os.path.join(dir_path_content, item)) and
                str(os.path.join(dir_path_content, item)).endswith(".md")):
            generate_page(os.path.join(dir_path_content, item), template_path, os.path.join(dest_dir_path, str(item)[0:-3]+".html"))
        else:
            moved = os.path.join(dir_path_content, item)
            generate_pages_recursive(moved, template_path, os.path.join(dest_dir_path, item))




























if __name__ == "__main__":
    main()
