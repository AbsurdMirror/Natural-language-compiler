import requests
import json
import re

from timer_library import Timer
from custom_print_library import *
from xml_parse import parse_xml_string


def parse_json_string(json_string):
    try:
        # 尝试将字符串解析为JSON对象
        json_object = json.loads(json_string)
        if not isinstance(json_object, dict):
            print_error("JSON object does not contain a dictionary.")
            return False
        if not '代码内容' in json_object:
            print_error("JSON object does not contain '代码内容' field.")
            return False
        if not '文件名' in json_object:
            print_error("JSON object does not contain '文件名' field.")
            return False
        return json_object
    except json.JSONDecodeError as e:
        # 捕获JSON解码错误并打印提示信息
        with open('DecodeErrorJSON.json', 'w') as f:
            f.write(json_string)
        print_error(f"JSON解析错误: {e}. See DecodeErrorJSON.json for details")
        return False

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
    url = f'https://agentapi.baidu.com/assistant/getAnswer?appId={app_id}&secretKey={secret_key}'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        "message": {
            "content": {
                "type": "text",
                "value": {
                    "showText": message_value
                }
            }
        },
        "source": source,
        "from": "openapi",
        "openId": open_id
    }

    request_count = 0
    request_count_max = 3
    while request_count < request_count_max:
      t = Timer().start_timing('Requesting AI response ...')
      response = requests.post(url, headers=headers, data=json.dumps(data))
      response_data = response.json()
      request_count += 1
      t.end_timing('Request finished.')

      if response.status_code == 200 and response_data['status'] == 0:
          ai_resp_data_str = response_data['data']['content'][0]['data']
          with open("code.xml", "w") as file:
              file.write(ai_resp_data_str)
          ai_resp_data = parse_xml_string(f"<回答>{ai_resp_data_str}</回答>")

          parse_fail = ai_resp_data == False
          parse_fail = parse_fail or '回答' not in ai_resp_data
          if parse_fail:
              with open("code.xml", "w") as file:
                  file.write(ai_resp_data_str)
              print_error("Error parsing XML response. See code.xml for details.")
              return False
          ai_resp_data = ai_resp_data['回答']
          parse_fail = parse_fail or '代码内容' not in ai_resp_data
          parse_fail = parse_fail or '文件名' not in ai_resp_data
          parse_fail = parse_fail or '代码语言' not in ai_resp_data
          if parse_fail:
              if request_count >= request_count_max:
                  print_error("Parsing XML response failed. Request count exceeded maximum limit.")
                  return False
              else:
                  print_warning("Parsing XML response failed. Requesting again...")
                  continue
          ai_resp_data = {
              '代码内容': ai_resp_data['代码内容']['#text'],
              '文件名': ai_resp_data['文件名']['#text'],
              '代码语言': ai_resp_data['代码语言']['#text']
          }
          print_info(f"Generated code type: {ai_resp_data['代码语言']}")
          with open("code.json", "w") as file:
              file.write(json.dumps(ai_resp_data))
          return ai_resp_data

      else:
          print_error(f"Error: Status: {response_data['status']}, Message: {response_data['message']}")
          print_error("See https://agents.baidu.com/docs/develop/out-deployment/API_calls")
          return False

def compile_by_ai_baidu(model_speed, message_value):
    # 三个百度模型，速度不一样
    models = {
        'fastest': {
            "app_id" : "rebsQWsNmqNzkIbjVj3fFDejGPAnpkFM",
            "secret_key" : "u56SotogQ7j5zUszoMhg0ck6VQhG7l2z"
        },
        'normal': {
            "app_id" : "B4xQNbXmznRP0qIzl2N2ZD2VkH45ibSm",
            "secret_key" : "rV0aKl4EuHglHUbrxCPBO8MLd5Cen4Jf"
        },
        'slowest': {
            "app_id" : "XKJlEiHJLo2DOJ8yZZXbx6K8SCUTqj1h",
            "secret_key" : "2q7BXx4d41eJwTUpNrIL3bPaMrbiNMNk"
        }
    }

    if model_speed == 'auto':
        # 根据输入内容的长度选择模型，越长的输入内容选择越慢的模型
        # 阈值设定
        normal_threshold = 500
        slowest_threshold = 1000
        if len(message_value) > slowest_threshold:
            model_speed = 'slowest'
            print_info(f"Auto-detected model speed: slowest. Because input length({len(message_value)}) exceeds threshold of {slowest_threshold} characters.")
        elif len(message_value) > normal_threshold:
            model_speed = 'normal'
            print_info(f"Auto-detected model speed: normal. Because input length({len(message_value)}) exceeds threshold of {normal_threshold} characters.")
        else:
            model_speed = 'fastest'
            print_info(f"Auto-detected model speed: fastest. Because input length({len(message_value)}) is within threshold of {normal_threshold} characters.")
    elif model_speed not in models:
        print_error("Invalid model speed. Please choose from 'fastest', 'normal', or 'slowest'.")
        return False

    app_id = models[model_speed]['app_id']
    secret_key = models[model_speed]['secret_key']
    source = models[model_speed]['app_id']
    open_id = "my_baidu_open_id"

    print_info(f"Using model speed: {model_speed}")
    return send_baidu_request(app_id, secret_key, source, open_id, message_value)


# 使用示例
if __name__ == "__main__":
    model_speed = 'normal'
    message_value = """python。统计输入文件的总行数"""
    
    response = compile_by_ai_baidu(model_speed, message_value)
    print_info(response)