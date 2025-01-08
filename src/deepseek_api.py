import os
from openai import OpenAI

from timer_library import Timer
from custom_print_library import *
from custom_resp_parser import *

# 系统提示词
system_prompt = """
#角色规范
作为自然语言编译器，你的任务是将用户输入的自然语言转换为对应的代码。你需要理解用户的意图，并准确生成符合语法规则的代码。你需要支持多种编程语言，包括但不限于Python、Java、JavaScript等。你的代码中应该有足够的注释来说明。当遇到无法直接转换的语句时，你需要向用户解释原因，并尝试提供替代方案。

#思考规范
1. **语言识别**：首先，你需要识别用户输入的语言类型（如中文、英文等），并确认是否属于你支持的语言列表。
2. **意图理解**：根据用户输入的自然语言，理解其意图或功能需求。这可能涉及对语句的结构分析、关键词识别等。
3. **代码生成**：基于你的理解和目标编程语言的语法规则，生成对应的代码片段。确保代码逻辑清晰、易于理解，注释内容详细，注释的语言与用户输入语言相同。

#回复规范
1. **设计代码文件名**: 在生成代码后，给出代码的文件名，要求文件名称和代码内容有关系，文件后缀名符合代码语言。（如：代码文件名：xxx.py）
2. **输出格式**：采用以下固定格式输出，格式如下：
<文件名>xxxx.xx</文件名>
<代码语言>xxxx</代码语言>
<代码内容>
xxxx
xxxx
.....
xxxx
</代码内容>

3.**干练内容**：你的返回内容中只需要提供代码文件名、代码语言和具体代码，不要任何的说明文字         

"""


def compile_by_ai_deepseek(message_value):
    # 获取py文件自身路径
    # 打开keys/deepseek.txt文件，读取其中的内容作为API密钥
    file_path = os.path.abspath(__file__)
    file_path = os.path.dirname(file_path)
    try:
        with open(f"{file_path}/../keys/deepseek.txt", "r") as f:
            api_key = f.read()
            if not api_key:
                raise ValueError("No API key found in keys/deepseek.txt file.")
    except FileNotFoundError:
        raise FileNotFoundError("../keys/deepseek.txt file not found.")

    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message_value},
        ],
        max_tokens=1024,
        temperature=0.7,
        stream=False,
    )
    ai_resp_string = response.choices[0].message.content
    ai_resp_data = parse_custom_resp(ai_resp_string)
    if ai_resp_data is not None:
        print_info(f"Generated code type: {ai_resp_data['代码语言']}")
        return {
            "文件名": ai_resp_data["文件名"],
            "代码内容": ai_resp_data["代码内容"].strip()
        }
    else:
        print_error("Failed to generate code using AI.")
        return False
    # print(response.choices[0].message.content)
