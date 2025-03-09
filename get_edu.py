import os
import re
import time  # 引入 time 模块

def get_unique_urls_from_hosts(target_directory: str, edu_file: str, org_file: str, cn_file: str):
    # 获取文件夹中所有的文件和文件夹
    files = os.listdir(target_directory)
    
    # 存储所有的host
    edu_hosts = set()  # 存储包含 .edu 的host
    org_hosts = set()  # 存储包含 .org 的host
    cn_hosts = set()  # 存储包含 .cn 的host

    # 统计找到的txt文件数量
    file_count = 0
    
    # 遍历文件夹中的文件
    for file in files:
        file_path = os.path.join(target_directory, file)
        
        # 如果是txt文件
        if os.path.isfile(file_path) and file.endswith('.txt'):
            file_count += 1  # 增加文件计数
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                # 按行读取文件
                for line in f:
                    # 获取host, 假设每一行都是一个host
                    host = line.strip()
                    
                    # 移除 www 前缀
                    if host.startswith('www.'):
                        host = host[4:]  # Remove 'www.' from the beginning
                    
                    # 分类保存
                    if '.edu' in host:
                        edu_hosts.add(host)
                    elif '.org' in host:
                        org_hosts.add(host)
                    elif '.cn' in host:
                        cn_hosts.add(host)        
                
        # 打印处理进度
        progress = (file_count / len(files)) * 100  # 计算进度百分比
        print(f"处理进度: {file_count}/{len(files)} 文件 ({progress:.2f}%)", end='\r')

    # 将包含 .edu 的host 保存到 edu_file
    with open(edu_file, 'w', encoding='utf-8') as edu_f:
        for host in edu_hosts:
            edu_f.write(host + '\n')  # 每个host 写一行
    
    # 将包含 .org 的host 保存到 org_file
    with open(org_file, 'w', encoding='utf-8') as org_f:
        for host in org_hosts:
            org_f.write(host + '\n')  # 每个host 写一行

    with open(cn_file, 'w', encoding='utf-8') as cn_f:
        for host in cn_hosts:
            cn_f.write(host + '\n')  # 每个host 写一行

    print(f"\n包含 .edu 的host 已保存到 {edu_file}")
    print(f"包含 .org 的host 已保存到 {org_file}")

# 记录开始时间
start_time = time.time()

target_directory = "annotation-urls-target"  # 目标文件夹路径
edu_file = "edu_urls.txt"  # 保存包含 .edu 的host 的文件
org_file = "org_urls.txt"  # 保存包含 .org 的host 的文件
cn_file = "cn_urls.txt"  # 保存包含 .cn 的host 的文件

# 调用函数
get_unique_urls_from_hosts(target_directory, edu_file, org_file, cn_file)

# 记录结束时间
end_time = time.time()

# 计算所花费的时间
elapsed_time = end_time - start_time

# 输出花费的时间
print(f"执行时间: {elapsed_time:.2f} 秒")
