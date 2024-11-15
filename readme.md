# 自然语言编译器

## 功能

使用AI大模型，根据自然语言生成对应的编程代码

## 用法

### 基础用法

```shell
python .\src\nlc.py <input_file> [-o <output_file>]
```

```shell
python .\src\nlc.py .\examples\time_count\time_count.md
```

## AI模型

目前AI模型支持：
- 文心大模型：使用文心智能体平台创建的智能体

### 文心大模型

编译器默认使用文心大模型，也可使用 `--ai_model Baidu` 或者 `-a Baidu` 来指定。

文心智能体平台提供三种大模型：
- 文心极速模型
- 文心大模型3.5
- 文心大模型4.0

使用这三个模型分别创建了3个智能体。工具默认根据输入的自然语言长度来选择模型，也可以手动选择：
- 自动选择（默认） `--model_speed auto` 或者 `-m auto`
- 文心极速模型 `--model_speed fastest` 或者 `-m fastest`
- 文心大模型3.5 `--model_speed normal` 或者 `-m normal`
- 文心大模型4.0 `--model_speed slowest` 或者 `-m slowest`

建议：输入自然语言越长，选择速度越慢的（效果越好的）模型。

此外，使用相同的提示词创建了输出内容适合网页版的智能体：[自然语言编译器](https://agents.baidu.com/agent/preview/yxRicnXX1HQKdnQo57mmendqfvaSDKNW)

## 其他

生成的代码可能会有一些bug，需要手动修改。

生成的代码可能需要安装一些依赖，请自行安装。

生成的代码可能需要修改，请自行修改。
