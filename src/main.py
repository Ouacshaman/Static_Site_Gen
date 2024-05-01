from textnode import TextNode
import os
import shutil


def main():
    Init_node = TextNode("drunken fist", "bold", "www.google.com")
    print(Init_node)
    static_path = "/Users/shihong/Downloads/Code/Create/proj04/Static_Site_Gen/static/"
    public_path = "/Users/shihong/Downloads/Code/Create/proj04/Static_Site_Gen/public/"
    copy_static(static_path, public_path)


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


if __name__ == "__main__":
    main()



























