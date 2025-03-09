import os
import re
from urllib.parse import urlparse
import shutil
import time  # 引入 time 模块

def get_largest_txt_file_with_url(source_directory: str, target_directory: str):
    # 如果目标目录不存在，创建它
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
        print(f"目标目录 {target_directory} 已创建.")
    
    # 获取文件夹中所有的文件和文件夹
    files = os.listdir(source_directory)
    
    # 存储所有txt文件的路径和大小
    txt_files = []
    
    # URL 正则表达式
    url_pattern = re.compile(r'https?://\S+')
    
    # 统计找到的txt文件数量
    file_count = 0
    
    # 遍历文件夹中的文件
    for file in files:
        file_path = os.path.join(source_directory, file)
        
        # 如果是txt文件
        if os.path.isfile(file_path) and file.endswith('.txt'):
            file_count += 1  # 增加文件计数
            file_size = os.path.getsize(file_path)
            txt_files.append((file_path, file_size))
    
    # 按文件大小从大到小排序
    txt_files.sort(key=lambda x: x[1], reverse=True)
    
    # 当前已处理的文件数
    processed_files = 0
    
    # 遍历排序后的文件，按大小从大到小检查
    for file_path, file_size in txt_files:
        processed_files += 1  # 增加已处理文件计数
        unique_hosts = set()  # 存储不重复的host
        url_count = 0
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            # 按行读取文件
            for line in f:
                urls = url_pattern.findall(line)  # 查找当前行中的所有 URL
                for url in urls:
                    url_count += 1
                    parsed_url = urlparse(url)
                    
                    # 如果 netloc 包含 '{'，则跳过这个 URL
                    if '{' in parsed_url.netloc:
                        print(f"跳过无效 URL (包含 '{{') in file: {file_path}, URL: {url}")
                        continue
                    
                    unique_hosts.add(parsed_url.netloc)  # 获取域名并添加到集合中
        
        # 如果包含 URL，则将不重复的域名写入新的文件
        if url_count > 0:
            hosts_file_path = os.path.join(target_directory, os.path.basename(file_path).replace('.txt', '_hosts.txt'))
            with open(hosts_file_path, 'w', encoding='utf-8') as hosts_file:
                for host in unique_hosts:
                    hosts_file.write(host + '\n')  # 每个域名写一行
        
        # 打印处理进度
        progress = (processed_files / file_count) * 100  # 计算进度百分比
        print(f"处理进度: {processed_files}/{file_count} 文件 ({progress:.2f}%)", end='\r')


# 记录开始时间
start_time = time.time()

source_directory = "annotation-urls-main"  # 修改为源文件夹的实际路径
target_directory = "annotation-urls-target"  # 修改为目标文件夹的实际路径

# 调用函数
get_largest_txt_file_with_url(source_directory, target_directory)

# 记录结束时间
end_time = time.time()

# 计算所花费的时间
elapsed_time = end_time - start_time

# 输出花费的时间
print(f"\n执行时间: {elapsed_time:.2f} 秒")
