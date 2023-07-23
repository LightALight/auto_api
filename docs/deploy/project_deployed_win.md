# 自动化环境安装和运行：window

* [pipenv安装部署](#部署工程)
* [使用](#使用)
* [问题处理](#问题处理)

## 前置工作

### git
* 登录[官网下载](https://git-scm.com/download/win)点击下载
* 下载完安装即可
* 配置用户名和邮箱

```bash
git config --global user.name "王重阳"
git config --global user.email chongyang_wang@example.com
```

### python3.11
* 登录[官网下载](https://www.python.org/downloads/)选择*Windows x86-64 executable installer*下载
* 下载完安装即可

### allure
* 进入[网站下载](https://github.com/allure-framework/allure2/releases)
* 选择某个目录解压即可使用



## 部署工程

* 步骤1：此电脑-属性-高级系统设置-系统属性-环境变量-新建
    ```dos
    变量名：WORKON_HOME
    变量值：PIPENV_VENV_IN_PROJECT
    ``` 
* 步骤2：更新pip版本
    ```dos
    python -m pip install --upgrade pip
    ```
* 步骤3：安装pipenv
    ```dos
    pip install pipenv==2022.8.24
    ```
* 步骤4：将项目clone到本地
    ```dos
    git clone git@github.com:LightALight/auto_api.git
    ```   
* 步骤5：进入到该项目录，根据python版本为该项目生成虚拟环境
    ```dos
    cd suiyunuitest
    pipenv --python 3.8
    ```
* 步骤6：一键安装项目所需要的库
    ```dos
    pipenv install  --skip-lock
    ```
* 步骤7：使用该项目虚拟环境的常用命令
    ```dos
    rem 方法1:进入虚拟环境执行命令
    pipenv shell
    
    rem 方法2:选择虚拟环境执行命令
    pipenv run python
    ```
* 步骤8：IDE选择使用编译器，在工程目录下的PIPENV_VENV_IN_PROJECT/[虚拟环境名称]/Scripts/python.exe



##  问题处理

* 1.生成虚拟环境，报错“invalid continuation byte”
    * 原因： 因为windows默认GBK编码，所以报错
    * 解决方法：修改报错位置的编码方式utf-8为gbk
