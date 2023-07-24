## 简介

- 通过swagger json(目前只适合Yaapi导出) 自动生成Api方法和冒烟测试用例
- pytest 管理运行测试用例
- allure 生成测试报告


## 框架结构说明

- **api_gen** swagger生成api
- **common** 文件夹是放置一些公共基类方法，方便其他模块调用
- **config** 文件夹是放置一些脚本执行需要用到的配置信息
- **docs** 文件夹是安装文档说明和依赖文件
- **report** 文件夹是放置日志和测试报告
- **testcases** 文件夹是放置测试用例模块
- **run.py** 文件是封装的执行入口，支持传参执行用例脚本


## 代码格式规范

代码编写格式需符合 python 的 PEP8 规范

## 生成代码

```bash
# 读取 docs 的api文档,写入common的api和testcases里面test_smoke生成冒烟用例
python3 code_gen.py
```

## 代码运行

```bash
python3 run.py
```


## 文档

- [windows部署文档](docs/deploy/project_deployed_win.md)
