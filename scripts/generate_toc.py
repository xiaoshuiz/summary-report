import os
from datetime import datetime

def get_md_title(md_file_path):
    """读取 Markdown 文件的第一行 H1 标题。"""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('# '):
                    return line[2:].strip()
    except Exception:
        # 如果读取文件失败或没有找到 H1，则返回 None
        pass
    return None

def update_readme_toc(readme_path, toc_content):
    """更新 README 文件中的目录部分。"""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"错误: README 文件未找到于 {readme_path}")
        return

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
        new_lines.append('\n') 
        new_lines.extend([f"{line}\n" for line in toc_content])
        new_lines.append('\n') 
        new_lines.extend(lines[toc_end_index:])
        
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"目录已成功更新到 {readme_path}")
    else:
        # 保持现有行为，如果标记未找到则打印错误
        print(f"错误：在 {os.path.basename(readme_path)} 中未找到 '<!-- TOC_START -->' 或 '<!-- TOC_END -->' 标记。")

def get_date_from_dir_name(dir_name_str):
    """尝试从目录名字符串中解析 YYYY-MM-DD 格式的日期。"""
    try:
        return datetime.strptime(dir_name_str, "%Y-%m-%d").date()
    except ValueError:
        return None

def generate_toc_for_directory(current_dir_abs, knowledge_root_abs, level=0):
    toc_lines = []
    
    # 特殊处理 knowledge 根目录 (level 0)
    if level == 0 and os.path.normpath(current_dir_abs) == os.path.normpath(knowledge_root_abs):
        date_dir_names = []
        other_item_names = [] # 包括非日期格式的文件夹和文件

        for item_name in os.listdir(current_dir_abs):
            if item_name.startswith('.'):
                continue
            item_full_abs_path = os.path.join(current_dir_abs, item_name)
            if os.path.isdir(item_full_abs_path) and get_date_from_dir_name(item_name):
                date_dir_names.append(item_name)
            else:
                other_item_names.append(item_name)
        
        # 日期文件夹按日期倒序排列
        date_dir_names.sort(key=lambda name: get_date_from_dir_name(name), reverse=True)
        # 其他项按字母顺序排列
        other_item_names.sort()

        # 首先处理排序后的日期文件夹
        for dir_name in date_dir_names:
            item_abs_path = os.path.join(current_dir_abs, dir_name)
            relative_path = os.path.relpath(item_abs_path, start=knowledge_root_abs).replace("\\\\", "/")
            indent = '  ' * level
            # 对日期文件夹，我们使用其本身的名字作为标题
            toc_lines.append(f"{indent}- [{dir_name}](./knowledge/{relative_path}/)")
            toc_lines.extend(generate_toc_for_directory(item_abs_path, knowledge_root_abs, level + 1))
        
        # 然后处理其他文件和文件夹
        for item_name in other_item_names:
            item_abs_path = os.path.join(current_dir_abs, item_name)
            relative_path = os.path.relpath(item_abs_path, start=knowledge_root_abs).replace("\\\\", "/")
            indent = '  ' * level
            
            if os.path.isdir(item_abs_path):
                toc_lines.append(f"{indent}- [{item_name}](./knowledge/{relative_path}/)")
                toc_lines.extend(generate_toc_for_directory(item_abs_path, knowledge_root_abs, level + 1))
            elif item_name.endswith('.md'):
                title = get_md_title(item_abs_path) or os.path.splitext(item_name)[0]
                toc_lines.append(f"{indent}- [{title}](./knowledge/{relative_path})")
            
    else: 
        # 对于子目录（包括日期文件夹内部，或其他非日期文件夹内部）
        # 标准字母排序
        try:
            list_of_items = os.listdir(current_dir_abs)
        except FileNotFoundError: # 以防万一，如果目录在遍历过程中被删除
            return toc_lines 

        item_names_in_subdir = sorted(list_of_items)
        for item_name in item_names_in_subdir:
            if item_name.startswith('.'):
                continue
            
            item_abs_path = os.path.join(current_dir_abs, item_name)
            # relative_path 始终相对于 knowledge_root_abs
            relative_path = os.path.relpath(item_abs_path, start=knowledge_root_abs).replace("\\\\", "/")
            indent = '  ' * level

            if os.path.isdir(item_abs_path):
                toc_lines.append(f"{indent}- [{item_name}](./knowledge/{relative_path}/)")
                toc_lines.extend(generate_toc_for_directory(item_abs_path, knowledge_root_abs, level + 1))
            elif item_name.endswith('.md'):
                title = get_md_title(item_abs_path) or os.path.splitext(item_name)[0]
                toc_lines.append(f"{indent}- [{title}](./knowledge/{relative_path})")
    return toc_lines

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    knowledge_dir_abs = os.path.abspath(os.path.join(script_dir, '../knowledge'))
    readme_file_abs = os.path.abspath(os.path.join(script_dir, '../README.md'))

    if not os.path.exists(knowledge_dir_abs):
        print(f"错误：找不到 '{os.path.basename(knowledge_dir_abs)}' 目录 ({knowledge_dir_abs})。请先创建它并添加您的知识文件。")
    elif not os.path.isdir(knowledge_dir_abs):
         print(f"错误：'{os.path.basename(knowledge_dir_abs)}' ({knowledge_dir_abs}) 不是一个目录。")
    else:
        toc = generate_toc_for_directory(knowledge_dir_abs, knowledge_dir_abs, level=0)
        update_readme_toc(readme_file_abs, toc) 