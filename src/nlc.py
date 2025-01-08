import sys
import chardet
import argparse

from custom_print_library import *
from baidu_api import *
from deepseek_api import *
from write_code_file import *


parser = argparse.ArgumentParser(description="自然语言编译器")

# 添加位置参数：输入的文件路径
parser.add_argument("input_file_path", help="自然语言源文件的路径")

# 添加可选参数：AI模型
parser.add_argument("--ai_model", "-a", help="AI模型，默认为'Baidu'", default="Baidu")

# 添加可选参数：使用baiduAI模型时，指示模型速度
parser.add_argument(
    "--model_speed", "-m", help="AI模型速度，默认为'auto'", default="auto"
)

# 添加可选参数：输出文件路径
parser.add_argument(
    "--output_file_path", "-o", help="输出文件的路径，默认为'output.txt'", default=""
)

# 添加可选参数：debug模式
parser.add_argument(
    "--debug", "-d", help="是否启用调试模式，默认为False", action="store_true"
)

# 解析命令行参数
args = parser.parse_args()


# 判断文件是否存在，读取文件内容
input_file_path = args.input_file_path
if not os.path.isfile(input_file_path):
    print_error(f": File '{input_file_path}' does not exist.")
    exit(1)

# 检测文件编码
encoding = chardet.detect(open(input_file_path, "rb").read())["encoding"]

# 使用检测到的编码打开文件
with open(input_file_path, "r", encoding=encoding) as f:
    input_text = f.read()

# debug输出
if args.debug:
    print_debug(f"Input text: {input_text}")

# 根据ai模型调用对应的api
if args.ai_model == "Baidu":
    print_info(f"Compiling with AI model '{args.ai_model}' ...")
    resp_data = compile_by_ai_baidu(args.model_speed, input_text)
elif args.ai_model == "DeepSeek":
    print_info(f"Compiling with AI model '{args.ai_model}' ...")
    resp_data = compile_by_ai_deepseek(input_text)
else:
    print_error(f"Unsupported AI model '{args.ai_model}'.")
    exit(1)

if not resp_data:
    print_error(" Failed to get response")
    exit(1)
elif not ("文件名" in resp_data and "代码内容" in resp_data):
    print_error(" Invalid response data from Baidu API.")
    print_error(f"Response data:")
    print_error(resp_data.json())
    exit(1)
else:
    # debug输出
    if args.debug:
        print_debug(f"Response data:")
        print_debug(resp_data.json())

    default_output_file_path = os.path.join(
        os.path.dirname(input_file_path), resp_data["文件名"]
    )
    output_file_path = (
        args.output_file_path if args.output_file_path else default_output_file_path
    )

    # debug输出
    if args.debug:
        print_debug(f"default_output_file_path: {default_output_file_path}")
        print_debug(f"args.output_file_path: {args.output_file_path}")
        print_debug(f"output_file_path: {output_file_path}")

    output_file_path = write_code_to_file(output_file_path, resp_data["代码内容"])
    print_info(f"Compiled successfully. Output file: {output_file_path}")
    exit(0)
