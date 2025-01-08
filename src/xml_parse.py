import xml.etree.ElementTree as ET

def xml_to_dict(element):
    """
    将XML元素转换为字典
    """
    dict_item = {}
    
    # 遍历子元素
    for child in element:
        child_dict = xml_to_dict(child)
        tag = child.tag
        
        # 如果字典中已经有这个键，并且是一个列表，则继续添加
        if tag in dict_item:
            if isinstance(dict_item[tag], list):
                dict_item[tag].append(child_dict)
            else:
                dict_item[tag] = [dict_item[tag], child_dict]
        else:
            dict_item[tag] = child_dict
    
    # 处理文本内容
    if element.text and element.text.strip():
        dict_item['#text'] = element.text.strip()
    
    # 如果这个元素没有子元素，则直接返回文本内容（如果有）
    if not dict_item:
        return element.text.strip() if element.text and element.text.strip() else None
    
    return dict_item

def parse_xml_string(xml_string):
    """
    将XML字符串解析为字典
    """
    root = ET.fromstring(xml_string)
    return {root.tag: xml_to_dict(root)}

# 示例使用
if __name__ == '__main__':

  # 示例XML字符串
  # xml_string = """
  # <note>
  #     <to>Tove</to>
  #     <from>Jani</from>
  #     <heading>Reminder</heading>
  #     <body>Don't forget me this weekend!</body>
  # </note>
  # """
  with open("./examples/code.xml", "r") as f:
      xml_string = f.read()

  # 解析XML字符串并转换为字典
  result_dict = parse_xml_string(xml_string)
  print(result_dict)