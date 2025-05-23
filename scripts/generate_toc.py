import os

def generate_toc_for_directory(directory_path, level=0):
    """递归生成指定目录的 Markdown 目录列表。"""
    toc_lines = []
    items = sorted(os.listdir(directory_path))
    for item in items:
        if item.startswith('.'):  # 忽略隐藏文件和目录
            continue
        item_path = os.path.join(directory_path, item)
        # 将绝对路径转换为相对于 knowledge 目录的路径
        relative_item_path = os.path.relpath(item_path, start='knowledge').replace("\\", "/")
        indent = '  ' * level
        if os.path.isdir(item_path):
            toc_lines.append(f"{indent}- [{item}](./knowledge/{relative_item_path}/)")
            toc_lines.extend(generate_toc_for_directory(item_path, level + 1))
        elif item.endswith('.md'):
            # 移除 .md 后缀以获得更清晰的链接标题
            file_name_without_ext = os.path.splitext(item)[0]
            toc_lines.append(f"{indent}- [{file_name_without_ext}](./knowledge/{relative_item_path})")
    return toc_lines

def update_readme_toc(readme_path, toc_content):
    """更新 README 文件中的目录部分。"""
    with open(readme_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    toc_start_index = -1
    toc_end_index = -1

    for i, line in enumerate(lines):
        if '<!-- TOC_START -->' in line:
            toc_start_index = i
        elif '<!-- TOC_END -->' in line:
            toc_end_index = i
            break
    
    if toc_start_index != -1 and toc_end_index != -1:
        new_lines = lines[:toc_start_index + 1]
        new_lines.append('\n') # 确保TOC_START 和实际内容之间有空行
        new_lines.extend([f"{line}\n" for line in toc_content])
        new_lines.append('\n') # 确保实际内容和TOC_END之间有空行
        new_lines.extend(lines[toc_end_index:])
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"目录已成功更新到 {readme_path}")
    else:
        print("错误：在 README.md 中未找到 '<!-- TOC_START -->' 或 '<!-- TOC_END -->' 标记。")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    knowledge_dir = os.path.join(script_dir, '../knowledge')
    readme_file = os.path.join(script_dir, '../README.md')

    # 确保 knowledge 目录存在
    if not os.path.exists(knowledge_dir):
        print(f"错误：找不到 '{knowledge_dir}' 目录。请先创建它并添加您的知识文件。")
    else:
        # 生成目录内容
        toc = generate_toc_for_directory(knowledge_dir)
        
        # 更新 README
        update_readme_toc(readme_file, toc) 