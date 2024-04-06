# Financial Log Tool X -- *FLTX*

## 日志
1. 2024年3月12日 **FLTX** 立项
2. 2024年3月27日 修改 ***readme.md*** ，以更清楚地介绍程序
3. 2024年3月30日 新增 ***fltx-gui-with-cli.py*** ，标志着 **FLTX** 开始建立GUI界面；修改***readme.md***，补充介绍 ***fltx-gui-with-cli.py***
4. 2024年4月5日 新增 ***fltx-gui.py*** ，标志着 **FLTX** 实现命令行代码与 *tkinter* 界面代码的合并；重写 ***readme.md*** 以更清楚地介绍程序

## 简介

一个简单的命令行程序，实现简单的账单统计。

基于命令行的 *tkinter* 界面已经建立，配合命令行使用。

无需命令行的 *tkinter* 界面已经建立，无需命令行即可使用。

## 使用教程

命令行：
```
配置好命令行的环境变量PATH后，即可在命令行当前目录下建表。

# 添加账单
fltx add [-h] [-d DATE] [-cp COUNTERPARTY] [-n NOTE] [-f FILE] path reason amount

# 删除账单
fltx delete [-h] [-f FILE] transaction_id

# 查找账单
fltx find [-h] [-f FILE] keyword

# 枚举账单
fltx list [-h] [-f FILE]

# 修改账单
fltx modify [-h] -fd {path,reason,amount,date,counterparty,note} -n NEW [-f FILE] transaction_id

# 统计账单
fltx statistics [-h] [-f FILE]
```

基于命令行的 *tkinter* 界面：

```
将命令行配置好后，运行该程序，即可在当前目录下建表。
点击需要使用的方法按钮，输入参数后，点击submit提交，即可在输出栏看到运行结果。
```

无需命令行的 *tkinter* 界面：

```
运行该程序，即可在当前目录下建表。
点击需要使用的方法按钮，输入参数后，点击submit提交，即可在输出栏看到运行结果。
```

## 说明

目前程序使用JSON格式保存账单，文件名为 ***sheet-XXXX-X.json*** ，样例如下：

```json
[
  {
    "id": 114514,
    "date": "2024-4-4-04:44:44",
    "reason": "锟斤拷",
    "amount": "19198.10",
    "path": "锟斤拷",
    "counterparty": "锟斤拷锟斤拷",
    "note": "锟斤拷锟斤拷"
  }
]
```

## 联系

我们衷心希望，各位开发者朋友能够与我们一起，开发更加便捷好用的账单处理程序。

如您有生动新奇的想法和建议，欢迎同我们联系。

邮箱：[BoogonClothman@outlook.com](mailto:BoogonClothman@outlook.com)
