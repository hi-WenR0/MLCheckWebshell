# coding:utf-8
# author: WenR0

import os
import re
import subprocess


def load_php_opcode(phpfilename):
    """
    获取php opcode 信息
    :param phpfilename:
    :return:
    """
    try:
        output = subprocess.check_output(['php.exe', '-dvld.active=1', '-dvld.execute=0', phpfilename], stderr=subprocess.STDOUT)
        tokens = re.findall(r'\s(\b[A-Z_]+\b)\s', output)
        t = " ".join(tokens)
        return t
    except:
        return " "



def recursion_load_php_file_opcode(dir):
    """
    递归获取 php opcde
    :param dir: 目录文件
    :return:
    """
    files_list = []
    for root, dirs, files in os.walk(dir):
        for filename in files:
            if filename.endswith('.php'):
                try:
                    full_path = os.path.join(root, filename)
                    file_content = load_php_opcode(full_path)
                    print "[Gen success] {}".format(full_path)
                    print '--' * 20
                    files_list.append(file_content)
                except:
                    continue
    return files_list