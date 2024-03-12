# Financial Log Tool X

2024

## 简介

一个简单的命令行工具，实现简单的账务日志统计

## 使用方法

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

## 配置

将fltx.exe下载到合适位置，设置环境变量，即可在任意目录下建表

## 说明

目前该程序采用了JSON格式保存，文件名为```sheet-{年}-{月}.json```，样例如下：
```json
[
    {
        "id": 1, // 整数
        "date": "2024-03-01-12:00:00", // 字符串
        "reason": "锟斤拷锟斤拷", // 字符串
        "amount": "-114.00", // 字符串
        "path": "锟斤拷", // 字符串
        "counterparty": "锟斤拷锟斤拷", // 字符串
        "note": "锟斤拷锟斤拷" // 字符串
    }
]
```

## 联系我

邮箱：[BoogonClothman@outlook.com](mailto:BoogonClothman@outlook.com)

Bilibili: [BoogonClothman](https://space.bilibili.com/3546377082636530)

