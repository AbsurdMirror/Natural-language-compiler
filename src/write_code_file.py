import os
import time
import random
import string

from custom_print_library import *

def generate_random_string(length=8):
    """生成指定长度的随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_unique_filename(base_filename):
    """获取一个唯一的文件名，并将内容写入文件"""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = base_filename

    # 获取路径
    filepath = os.path.dirname(filename)
    
    # 获取文件名（带后缀）
    file_name_with_ext = os.path.basename(filename)
    
    # 获取文件名（不带后缀）
    file_name_without_ext = os.path.splitext(file_name_with_ext)[0]
    
    # 获取文件后缀
    file_ext = os.path.splitext(file_name_with_ext)[1]

    # 确保文件夹存在
    if not os.path.exists(filepath):
        os.makedirs(filepath)

    counter = 0
   
    while os.path.exists(filename):
        counter += 1
        if counter == 1:
            # 第一次重名，添加时间后缀
            filename = os.path.join(filepath, f"{file_name_without_ext}_{timestamp}{file_ext}")
        else:
            # 后续重名，添加时间后缀和随机字符
            random_str = generate_random_string()
            filename = os.path.join(filepath, f"{file_name_without_ext}_{timestamp}_{random_str}{file_ext}")

    return filename

def write_code_to_file(filename, code_content):
    """主函数：将代码内容写入文件名"""
        
    filename = get_unique_filename(filename)

    # 将代码内容写入文件
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(code_content)
    
    return filename

# 示例使用
if __name__ == "__main__":
  filename = "my/path/example.txt"
  code_content = "```\nprint('Hello, World!')\n```"
  final_filename = write_code_to_file(filename, code_content)
  print_info(f"Code has been written to {final_filename}")