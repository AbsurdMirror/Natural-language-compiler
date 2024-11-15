# python 脚本库

## 库函数

- 提供两个函数，分别用于开始计时和结束计时
- 设计两个函数的名称

## 具体功能

### 开始计时

- 从当前时间开始计时
- 命令行显示:
  - 一个旋转的圆圈的加载动画的一个字符
  - 一个字符串，该字符串为输入参数
  - 字符串后显示一个计时秒表，格式: `[0.0s]`
  - 例如 "Loading Files ... [0.0s]"
- 函数返回一个对象，用于结束计时
- 函数返回后，计时不停，并且不影响后续代码的执行

### 结束计时

- 接受一个对象，该对象为开始计时函数返回的对象
- 结束计时
- 命令行显示:
  - 一个字符串，该字符串为输入参数
  - 字符串后显示一个总耗时，格式: `[Use 1.4s]`
  - 例如 "Loading Files Done [Use 1.4s]"

## 期望使用场景

```
库开始计时函数
做一些耗时的代码
库结束计时函数
```

效果：在命令行显示开始计时的信息，并且秒表持续更新，耗时的工作也同时进行，等到耗时工作完成后，命令行结束秒表显示，显示出总耗时
