import os
import re
import time  # 引入 time 模块
from urllib.parse import urlparse


class InvalidURLException(Exception):
    """自定义异常，用于处理无效的 URL"""
    def __init__(self, message, file_path, line_number):
        super().__init__(message)
        self.file_path = file_path
        self.line_number = line_number


def is_valid_host(host: str) -> bool:
    """验证主机名是否有效，检查是否包含下划线"""
    return '/' not in host




def get_unique_urls_from_hosts(target_directory: str, output_file: str, max_files: int):
    # 获取文件夹中所有的文件和文件夹
    files = os.listdir(target_directory)
    
    # 存储所有的 URL
    unique_urls = set()
    
    # 统计找到的txt文件数量
    file_count = 0
    
    # 遍历文件夹中的文件
    for file in files:
        if file_count >= max_files:
            break  # 如果已处理文件数量达到最大限制，退出循环
        
        file_path = os.path.join(target_directory, file)
        
        # 如果是txt文件
        if os.path.isfile(file_path) and file.endswith('.txt'):
            file_count += 1  # 增加文件计数
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # 按行读取文件
                for line_num, line in enumerate(f, start=1):
                    # 获取 URL, 假设每一行都是一个 URL
                    url = line.strip()
                    if url:
                        # 验证 URL 是否有效
                        if not  is_valid_host(url):
                            raise InvalidURLException(f"无效的 URL: {url}", file_path, line_num)
                        unique_urls.add(url)
                        # print(f"有效的 URL: {url}")  # 打印每个有效的 URL
        
        # 打印处理进度
        print(f"已处理文件: {file_count}/{max_files}", end='\r')

    # 将所有不重复的 URL 保存到 output_file
    with open(output_file, 'w', encoding='utf-8') as output_f:
        for url in unique_urls:
            output_f.write(url + '\n')  # 每个 URL 写一行
    
    print(f"\n所有不重复的 URL 已保存到 {output_file}")


def count_files_in_directory(directory: str):
    # 获取文件夹中所有的文件和文件夹
    files = os.listdir(directory)
    
    # 计算文件数量（只计算文件，不计算文件夹）
    file_count = sum(1 for file in files if os.path.isfile(os.path.join(directory, file)))
    
    return file_count

# 记录开始时间
start_time = time.time()

target_directory = "annotation-urls-target"  # 目标文件夹路径
output_file = "unique_urls.txt"  # 输出文件路径

try:
    # 调用函数，只处理前 100 个文件
    get_unique_urls_from_hosts(target_directory, output_file, max_files=count_files_in_directory(target_directory))
except InvalidURLException as e:
    print(f"错误：在文件 {e.file_path} 的第 {e.line_number} 行发现无效的 URL: {e}")
    # 你可以根据需要在这里处理错误，如记录日志或停止执行

# 记录结束时间
end_time = time.time()

# 计算所花费的时间
elapsed_time = end_time - start_time

# 输出花费的时间
print(f"执行时间: {elapsed_time:.2f} 秒")
