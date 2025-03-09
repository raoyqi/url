import os
import shutil
import re

def get_file_info(directory):
    # 获取文件夹中所有的文件和文件夹
    files = os.listdir(directory)
    
    # 用于存储文件类型
    file_types = {}
    
    # 计数文件数量
    file_count = 0
    
    # 存储最大的txt文件
    max_txt_file = None
    max_txt_size = 0
    
    # 遍历文件夹中的文件
    for file in files:
        file_path = os.path.join(directory, file)
        
        # 如果是文件
        if os.path.isfile(file_path):
            file_count += 1
            file_extension = os.path.splitext(file)[1]  # 获取文件扩展名
            if file_extension in file_types:
                file_types[file_extension] += 1
            else:
                file_types[file_extension] = 1
            
            # 如果是txt文件，检查其大小
            if file_extension == '.txt':
                file_size = os.path.getsize(file_path)
                if file_size > max_txt_size:
                    max_txt_size = file_size
                    max_txt_file = file_path
    
    return file_count, file_types, max_txt_file

def is_url(text):
    # 使用正则表达式检查文本是否为URL
    url_pattern = re.compile(
        r'^(https?://)?(www\.)?([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}(\/[a-zA-Z0-9_-]*)*(\?[a-zA-Z0-9_=&]*)?(#[a-zA-Z0-9_-]*)?$'
    )
    return re.match(url_pattern, text) is not None

def check_urls_in_file(file_path):
    all_urls = True  # 假设所有行都是URL
    total_lines = 0
    non_url_lines = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            total_lines += 1
            line = line.strip()  # 去除两端空白字符
            if not is_url(line):  # 如果有一行不是URL
                non_url_lines += 1
                print(f"非URL行: {line}")
    
    return total_lines, non_url_lines

def copy_largest_txt_file(source_directory, target_directory):
    # 获取文件信息
    file_count, file_types, max_txt_file = get_file_info(source_directory)
    
    print(f"文件数量: {file_count}")
    print("文件类型及数量:")
    for ext, count in file_types.items():
        print(f"{ext}: {count}")
    
    # if max_txt_file:
    #     print(f"\n最大的txt文件是: {max_txt_file}")
        
    #     # 检查文件内容
    #     total_lines, non_url_lines = check_urls_in_file(max_txt_file)
        
        # 输出文件中的统计信息
        # print(f"\n文件总行数: {total_lines}")
        # print(f"非URL行数: {non_url_lines}")
        
        # # 创建保存统计信息的文本文件
        # result_file = os.path.join(target_directory, "file_statistics.txt")
        
        # with open(result_file, 'w', encoding='utf-8') as result:
        #     result.write(f"文件名: {os.path.basename(max_txt_file)}\n")
        #     result.write(f"总行数: {total_lines}\n")
        #     result.write(f"非URL行数: {non_url_lines}\n")
        
        # print(f"\n统计信息已保存到: {result_file}")
        
        # 确保目标文件夹存在
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
            
        
        # 复制文件到目标文件夹
        target_path = os.path.join(target_directory, os.path.basename(max_txt_file))
        shutil.copy(max_txt_file, target_path)
        
        print(f"\n已将最大txt文件复制到: {target_path}")
    else:
        print("没有找到txt文件。")

# 示例：使用该函数读取文件夹中的文件并将最大的txt文件复制到另一个文件夹
source_directory = "annotation-urls-main"  # 修改为源文件夹的实际路径
target_directory = "annotation-urls-target"  # 修改为目标文件夹的实际路径
copy_largest_txt_file(source_directory, target_directory)
