# Financial Log Tool X

日志：

1. 2024年3月12日建立
2. 2024年3月27日修改readme文件
3. 2024年3月30日增加fltx-gui-with-cli.py文件，修改readme文件

## 简介

一个简单的命令行工具，实现简单的账务日志统计

+-- 2024年3月30日新增基于命令行工具的GUI界面

## 使用方法

仅使用命令行时：
```
fltx [-h] {add, delete, find, modify, list, statistics}

arguments:
  {add,delete,find,modify,list,statistics}
    add                 Add a new transaction.
    delete              Delete a transaction.
    find                Find transactions by keyword.
    modify              Modify a transaction.
    list                List all transactions.
    statistics          Show financial statistics.

options:
  -h, --help            show this help message and exit
```
配置好命令行的情况下，可以使用带有GUI界面的程序

此时只需点击上方的命令，输入必要参数，点击SUBMIT按钮即可看到结果


## 配置

将fltx.exe下载到合适位置，设置环境变量PATH，即可在任意目录下建表

## 说明

目前该程序采用了JSON格式保存，文件名为```sheet-{年}-{月}.json```，样例如下：
```json
[
    {
        "id": 114514,
        "date": "2024-03-27-20:00:00",
        "reason": "锟斤拷锟斤拷锟斤拷",
        "amount": "-19198.10",
        "path": "锟斤拷锟斤拷",
        "counterparty": "锟斤拷锟斤拷锟斤拷",
        "note": "锟斤拷锟斤拷锟斤拷"
    }
]
```

## 联系我

我们欢迎各位朋友，和我们一起开发更加好用的账务处理工具，也欢迎各位朋友提出更加生动有趣的想法。

个人邮箱：[BoogonClothman@outlook.com](mailto:BoogonClothman@outlook.com)

Bilibili: [BoogonClothman](https://space.bilibili.com/3546377082636530)
