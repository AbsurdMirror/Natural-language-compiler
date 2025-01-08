import requests
import json
import re
import os

from timer_library import Timer
from custom_print_library import *
from custom_resp_parser import *

def send_baidu_request(app_id, secret_key, source, open_id, message_value):
    """
    向百度API发送请求并返回响应

    参数:
    app_id (str): 应用ID
    secret_key (str): 密钥
    source (str): 来源
    open_id (str): 开放ID
    message_value (str): 消息内容

    返回:
    dict: 响应内容
    """
    url = f"https://agentapi.baidu.com/assistant/getAnswer?appId={app_id}&secretKey={secret_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "message": {"content": {"type": "text", "value": {"showText": message_value}}},
        "source": source,
        "from": "openapi",
        "openId": open_id,
    }

    request_count = 0
    request_count_max = 3
    while request_count < request_count_max:
        t = Timer().start_timing("Requesting AI response ...")
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response_data = response.json()
        request_count += 1
        t.end_timing("Request finished.")

        if response.status_code == 200 and response_data["status"] == 0:
            ai_resp_string = response_data["data"]["content"][0]["data"]
            ai_resp_data = parse_custom_resp(ai_resp_string)
            if ai_resp_data is not None:
                print_info(f"Generated code type: {ai_resp_data['代码语言']}")
                return {
                    "文件名": ai_resp_data["文件名"],
                    "代码内容": ai_resp_data["代码内容"].strip()
                }
            elif request_count >= request_count_max:
                print_warning(
                    "Response parse failed. Request count exceeded maximum limit."
                )
                return False
            else:
                print_warning("Response parse failed. Requesting again...")
                continue

            # with open("response.xml", "w") as f:
            #     f.write(ai_resp_data)
            # # 定义正则表达式
            # pattern = re.compile(
            #     r"<文件名>(.*?)</文件名>\s*<代码语言>(.*?)</代码语言>\s*<代码内容>(.*?)</代码内容>",
            #     re.DOTALL,
            # )
            # match = re.search(pattern, ai_resp_data)
            # if match:
            #     # print("文件名:", match[1])
            #     # print("代码语言:", match[2])
            #     # print("代码内容:", match[3])

            #     print_info(f"Generated code type: {match.group(2)}")
            #     return {
            #         "文件名": match[1],
            #         "代码内容": match[3].strip(),
            #     }
            # elif request_count >= request_count_max:
            #     print_warning(
            #         "Response parse failed. Request count exceeded maximum limit."
            #     )
            #     return False
            # else:
            #     print_warning("Response parse failed. Requesting again...")
            #     continue

            # for match in matches:
            #     print("文件名:", match[0])
            #     print("代码语言:", match[1])
            #     print(
            #         "代码内容:", match[2].strip()
            #     )  # 使用strip()去除可能的首尾空白字符
            #     print_info(f"Generated code type: {match.group(1)}")
            #     return {
            #         "文件名": match[0],
            #         "代码内容": match[2].strip(),
            #     }
            # # 正则表达式匹配 json Markdown 代码块
            # code_block_pattern = re.compile(r"```json\n(\{.*\})\n```", re.DOTALL)
            # match = re.search(code_block_pattern, ai_resp_data)
            # # print_info(match)
            # if match:
            #     ai_resp_data = match.group(1)
            # elif request_count >= request_count_max:
            #     print_warning(
            #         "No JSON code block found in the response. Request count exceeded maximum limit."
            #     )
            #     return False
            # else:
            #     print_warning(
            #         "No JSON code block found in the response. Requesting again..."
            #     )
            #     continue

            # # print_info(ai_resp_data)
            # ai_resp_data = parse_json_string(ai_resp_data)
            # if ai_resp_data == False:
            #     if request_count >= request_count_max:
            #         print_error(
            #             "Error parsing JSON response. Request count exceeded maximum limit."
            #         )
            #         return False
            #     else:
            #         print_error("Error parsing JSON response. Requesting again...")
            #         continue

            # # print_info(ai_resp_data)
            # # 正则表达式匹配 Markdown 代码块
            # code_block_pattern = re.compile(r"```(.*?)\n(.*?)```", re.DOTALL)
            # match = re.search(code_block_pattern, ai_resp_data["代码内容"])
            # # print_info("代码内容解析", match.group(2), match.group(1))
            # if match:
            #     ai_resp_data["代码内容"] = match.group(2)
            #     print_info(f"Generated code type: {match.group(1)}")
            #     # print_info(ai_resp_data)
            #     return ai_resp_data
            # else:
            #     if request_count >= request_count_max:
            #         print_warning(
            #             "No code block found in the response. Request count exceeded maximum limit."
            #         )
            #         return False
            #     else:
            #         print_warning(
            #             "No code block found in the response. Requesting again..."
            #         )
            #         continue
        else:
            print_error(
                f"Error: Status: {response_data['status']}, Message: {response_data['message']}"
            )
            print_error(
                "See https://agents.baidu.com/docs/develop/out-deployment/API_calls"
            )
            if request_count >= request_count_max:
                return False
            else:
                continue


def compile_by_ai_baidu(model_speed, message_value):
    # 三个百度模型，速度不一样
    # 读取文件
    file_path = os.path.abspath(__file__)
    file_path = os.path.dirname(file_path)
    try:
        with open(f"{file_path}/../keys/baidu.json", "r") as f:
            api_key = f.read()
            if not api_key:
                print_error("No API key found in keys/baidu.json file.")
                return False
    except FileNotFoundError:
        print_error("../keys/baidu.json file not found.")
        return False

    # 解析JSON字符串
    try:
        models = json.loads(api_key)
    except json.decoder.JSONDecodeError:
        print_error("Error: Invalid JSON format in keys/baidu.json file.")
        return False

    if model_speed == "auto":
        # 根据输入内容的长度选择模型，越长的输入内容选择越慢的模型
        # 阈值设定
        normal_threshold = 500
        slowest_threshold = 1000
        if len(message_value) > slowest_threshold:
            model_speed = "slowest"
            print_info(
                f"Auto-detected model speed: slowest. Because input length({len(message_value)}) exceeds threshold of {slowest_threshold} characters."
            )
        elif len(message_value) > normal_threshold:
            model_speed = "normal"
            print_info(
                f"Auto-detected model speed: normal. Because input length({len(message_value)}) exceeds threshold of {normal_threshold} characters."
            )
        else:
            model_speed = "fastest"
            print_info(
                f"Auto-detected model speed: fastest. Because input length({len(message_value)}) is within threshold of {normal_threshold} characters."
            )
    elif model_speed not in models:
        print_error(
            "Invalid model speed. Please choose from 'fastest', 'normal', or 'slowest'."
        )
        return False

    app_id = models[model_speed]["app_id"]
    secret_key = models[model_speed]["secret_key"]
    source = models[model_speed]["app_id"]
    open_id = "my_baidu_open_id"

    print_info(f"Using model speed: {model_speed}")
    return send_baidu_request(app_id, secret_key, source, open_id, message_value)


# 使用示例
if __name__ == "__main__":
    model_speed = "normal"
    message_value = """python。统计输入文件的总行数"""

    response = compile_by_ai_baidu(model_speed, message_value)
    print_info(response)
