# 机器学习检测Webshell

# 简介

提取PHP执行中的opcode，采用 opcode词袋 + tf-idf 进行关键信息提取

采用朴素贝叶斯算法进行训练。

进行 PHP WebShell 的检测。

# 部署

## step 1. Python环境部署

```
pip install -r requirements.txt
```

## step 2. PHP opcode 部署

    开启opcode模式

windows环境

```
1. 下载 vld.dll 插件并存放在php ext 目录下
2. 配置 php.ini 激活vld.dll 文件
```
[VLD.dll下载地址](http://pecl.php.net/package/vld/0.14.0/windows)

[PHP.ini 配置参考文章](http://blog.sina.com.cn/s/blog_4c8c58ce0102wi2h.html
)

# 第一次进行训练

    将白名单的文件放入到 white-list 文件夹中
    将黑名单文件放入到 black-list 文件夹中

进行第一次训练
```shell
python train.py
```
Note:

    避免每次生成opcode 的时间过长，每次训练完成后，会生成两个文件，black_opcodes.txt & white_opcodes.txt。

    如果有新的白名单文件或者黑名单文件加入，先删除掉black_opcodes.txt 和 white_opcodes.txt 文件，然后再次进行训练。

    训练完成后，会在save文件夹内，生成一个gnb.pkl文件，这个是训练好的缓存文件。


# 检测

检测单个文件
```
python check.py [filename]
```


# 重复训练

1. 提供训练集
在人工得到结果后，可以在white-list & black-list 文件夹中，添加已知的结果，再按照第一次训练的方法，进行再次训练。得到的结果便会更加准确。


# 数据集（参考）

白名单
- https://github.com/WordPress/WordPress
- https://github.com/typecho/typecho
- https://github.com/phpmyadmin/phpmyadmin
- https://github.com/laravel/laravel
- https://github.com/top-think/framework
- https://github.com/symfony/symfony
- https://github.com/bcit-ci/CodeIgniter
- https://github.com/yiisoft/yii2

黑名单
- https://github.com/tennc/webshell
- https://github.com/ysrc/webshell-sample
- https://github.com/xl7dev/WebShell