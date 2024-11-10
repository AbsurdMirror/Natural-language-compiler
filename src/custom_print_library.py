import sys
from termcolor import colored

# 全局变量定义
PREFIX_DEBUG = "DEBUG"
COLOR_DEBUG = "blue"

PREFIX_INFO = "INFO"
COLOR_INFO = "green"

PREFIX_WARNING = "WARNING"
COLOR_WARNING = "yellow"

PREFIX_ERROR = "ERROR"
COLOR_ERROR = "red"

# 原始print函数备份
original_print = print

# 基础函数
def print_color(color, prefix, *args, **kwargs):
    # 打印前缀
    original_print(colored(f"[{prefix}]", color), end=' ')
    # 打印后续内容
    for arg in args:
        original_print(colored(arg, color), end=' ')
    original_print(**kwargs)

# 特定预设函数
def print_debug(*args, **kwargs):
    print_color(COLOR_DEBUG, PREFIX_DEBUG, *args, **kwargs)
    
def print_info(*args, **kwargs):
    print_color(COLOR_INFO, PREFIX_INFO, *args, **kwargs)
    
def print_warning(*args, **kwargs):
    print_color(COLOR_WARNING, PREFIX_WARNING, *args, **kwargs)

def print_error(*args, **kwargs):
    print_color(COLOR_ERROR, PREFIX_ERROR, *args, **kwargs)

# 重写print函数
def print(*args, **kwargs):
    original_print(colored("WARNING: Use custom print functions instead of the original print!", "magenta"))
    original_print(*args, **kwargs)

# 入口点检查
if __name__ == "__main__":
    # 示例用法
    print_debug("This is a debug message.")
    print_info("This is an info message.")
    print_warning("This is a warning message.")
    print_error("This is an error message.")

    # 尝试直接使用print函数，应该会触发warning
    print("This should trigger a warning.")
