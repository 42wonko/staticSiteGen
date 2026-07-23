import os
import shutil

from copystatic import copy_files_recursive
from block_markdown import markdown_to_html_node
from inline_markdown import extract_title


dir_path_static = "./static"
dir_path_public = "./public"

in_file = "index.md"
out_file = "index.html"
paths = [("./content","./public"), ("./content/blog/glorfindel", "./public/blog/glorfindel"), ("./content/blog/tom", "./public/blog/tom"), ("./content/blog/majesty","./public/blog/majesty"), ("./content/contact","./public/contact")]
template_path = "./template.html"

#fp = "content/index.md"
#dt = "public/index.html"

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    markdown_file = open(from_path, "r")
    markdown = markdown_file.read()
    markdown_file.close()
    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()
    content = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    html_page = template.replace("{{ Title }}",title).replace("{{ Content }}", content.to_html())
    if dest_path != "":
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    dst_file = open(dest_path, "w")
    dst_file.write(html_page)
    dst_file.close()
    

def main() -> None:
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    for input_file_dir, output_file_dir in paths:
        input_file = os.path.join(input_file_dir,in_file)
        output_file = os.path.join(output_file_dir,out_file)
        generate_page(input_file, template_path, output_file)

main()

