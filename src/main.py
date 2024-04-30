from textnode import TextNode
import os
import shutil


def main():
    Init_node = TextNode("drunken fist", "bold", "www.google.com")
    print(Init_node)


main()


def copy_static(input_dir, target_dir):
    if not os.path.exists(target_dir):
        pass

