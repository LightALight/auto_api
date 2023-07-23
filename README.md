## 简介

- 通过swagger json 自动生成Api方法和冒烟测试用例
- pytest 管理运行测试用例
- allure 生成测试报告


## 框架结构说明

- **docs** 文件夹是安装文档说明和依赖文件
- **config** 文件夹是放置一些脚本执行需要用到的配置信息
- **common** 文件夹是放置一些公共基类方法，方便其他模块调用
- **testcases** 文件夹是放置测试用例模块
- **run.py** 文件是封装的执行入口，支持传参执行用例脚本
- **static** 文件夹是放置日志和测试报告

## 代码格式规范

代码编写格式需符合 python 的 PEP8 规范

## 生成Api代码

```bash
# 生成 iOS UI 界面元素定位代码
python puppet/api_gen puppet/android/page/pages/autogen
```

## 代码运行

```bash

# run smoke case:
python3 run_test.py

# run all case:
python3 run_test.py

# 开启报告网址：
allure serve --alluredir {report_path}/result
```


## 文档

- [windows部署文档](docs/deploy/project_deployed_win.md)
