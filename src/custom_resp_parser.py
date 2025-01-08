"""
将一个如下格式的长字符串转换为一个字典。 py语言

长字符串：
```
<文件名>xxxx.xx</文件名>
<代码语言>xxxx</代码语言>
<代码内容>
xxxx
xxxx
.....
xxxx
</代码内容>
```

字典：
```
{
    "文件名": "xxxx.xx",
    "代码语言": "xxxx",
    "代码内容": "xxxx\nxxxx\n.....\nxxxx"
}
```

"""

import re

def parse_custom_resp(long_string):
    # 定义正则表达式模式
    pattern = r'<文件名>(.*?)</文件名>\s*<代码语言>(.*?)</代码语言>\s*<代码内容>\s*(.*?)\s*</代码内容>'
    
    # 使用正则表达式匹配
    match = re.search(pattern, long_string, re.DOTALL)
    
    if match:
        # 提取匹配的组
        file_name = match.group(1)
        code_language = match.group(2)
        code_content = match.group(3).strip()  # 去除多余的空格
        
        # 构建字典
        result_dict = {
            "文件名": file_name,
            "代码语言": code_language,
            "代码内容": code_content
        }
        
        return result_dict
    else:
        return None

if __name__ == "__main__":
    # 示例长字符串
    long_string = """
    <文件名>example.py</文件名>
    <代码语言>Python</代码语言>
    <代码内容>
    def hello_world():
        print("Hello, World!")

    hello_world()
    </代码内容>
    """

    # 转换为字典
    result = parse_string_to_dict(long_string)
    print(result)