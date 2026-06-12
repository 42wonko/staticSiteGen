from os import listdir, mkdir
from os.path import exists, isdir, join
from shutil import copy, rmtree

import textnode

def create_dir(directory):
    pass


def copy_files(src_dir, dst_dir):
    dir_list = []
    print(f'-D- copying {src_dir} -> {dst_dir}')
    if (not exists(src_dir)):
        print(f'-E- The source directory <{src_dir}> does not exists. Exiting !')
        return

    if (not exists(dst_dir)):
        print(f'-D- {dst_dir} does not exist -> creating it.')
        mkdir(dst_dir)
    
    dir_list = listdir(src_dir)
    for entry in dir_list:
        if isdir(join(src_dir, entry)):
            copy_files(join(src_dir, entry), join(dst_dir, entry))
        else:
            print(f'-D- copy {join(src_dir, entry)} -> {join(dst_dir, entry)}')
            copy(join(src_dir, entry), dst_dir)


def main():
#    node = textnode.TextNode("This is some anchor text", textnode.TextType.TEXT_LINK,"https://www.boot.dev")
#    print(node)
    copy_files("static", "public")

if __name__ == "__main__":
    main()
