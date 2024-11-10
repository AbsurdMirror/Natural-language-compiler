import sys
import re

# 检查命令行参数
if len(sys.argv) != 2:
    print("Usage: python file_reader.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

# 初始化标记
instance_found = False
pattern_match_found = False
reg_found = False
assign_found = False
always_found = False

# 定义正则表达式
pattern = re.compile(r'\w+\s+x_\w+\s+\(')
reg_pattern = re.compile(r'\breg\b')
assign_pattern = re.compile(r'\bassign\b')
always_pattern = re.compile(r'\balways\b')

try:
    with open(filename, 'r') as file:
        for line in file:
            # 检查是否包含字符串 '&Instance'
            if '&Instance' in line:
                print("Found '&Instance' in line:", line.strip())
                instance_found = True
            
            # 检查是否匹配正则表达式
            if pattern.search(line):
                print("Pattern match found in line:", line.strip())
                pattern_match_found = True
            
            # 检查正则全词匹配是否存在单词 'reg'
            if reg_pattern.search(line):
                print("Found 'reg' in line:", line.strip())
                reg_found = True
            
            # 检查正则全词匹配是否存在单词 'assign'
            if assign_pattern.search(line):
                print("Found 'assign' in line:", line.strip())
                assign_found = True
            
            # 检查正则全词匹配是否存在单词 'always'
            if always_pattern.search(line):
                print("Found 'always' in line:", line.strip())
                always_found = True

# 打印文件是否存在 'reg', 'assign', 'always'
print("File contains 'reg':", reg_found)
print("File contains 'assign':", assign_found)
print("File contains 'always':", always_found)

except FileNotFoundError:
    print("File not found")
