# coding:utf-8
# author: WenR0

import os
from utils import recursion_load_php_file_opcode, load_php_opcode

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib


def prepare_data():
    """
    生成需要使用的数据，写入文件后，以供后面应用
    :return:
    """
    # 生成数据并写入文件
    if os.path.exists('white_opcodes.txt') is False:
        print '[Info] White opcodes doesnt exists ... generating opcode ..'
        white_opcodes_list = recursion_load_php_file_opcode('.\\white-list\\')
        with open('white_opcodes.txt', 'w') as f:
            for line in white_opcodes_list:
                f.write(line + '\n')
    else:
        print '[Info] White opcodes exists'

    if os.path.exists('black_opcodes.txt') is False:
        black_opcodes_list = recursion_load_php_file_opcode('.\\black-list\\')
        with open('black_opcodes.txt', 'w') as f:
            for line in black_opcodes_list:
                f.write(line + '\n')
    else:
        print '[Info] black opcodes exists'

    # 使用数据

    white_file_list = []
    black_file_list = []

    with open('black_opcodes.txt', 'r') as f:
        for line in f:
            black_file_list.append(line.strip('\n'))

    with open('white_opcodes.txt', 'r') as f:
        for line in f:
            white_file_list.append(line.strip('\n'))

    len_white_file_list = len(white_file_list)
    len_black_file_list = len(black_file_list)

    y_white = [0] * len_white_file_list
    y_black = [1] * len_black_file_list

    X = white_file_list + black_file_list
    y = y_white + y_black

    print '[Data status] ... ↓'
    print '[Data status] X length : {}'.format(len_white_file_list + len_black_file_list)
    print '[Data status] White list length : {}'.format(len_white_file_list)
    print '[Data status] black list length : {}'.format(len_black_file_list)
    # X raw data
    # y label
    return X, y


def method1():
    """
    countVectorizer + TF-IDF 整理数据
    朴素贝叶斯算法生成
    :return: None
    """
    X, y = prepare_data()

    cv = CountVectorizer(ngram_range=(3, 3), decode_error="ignore", token_pattern=r'\b\w+\b')
    X = cv.fit_transform(X).toarray()

    transformer = TfidfTransformer(smooth_idf=False)
    X = transformer.fit_transform(X).toarray()

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)

    gnb = GaussianNB()
    gnb.fit(x_train, y_train)
    joblib.dump(gnb, 'save/gnb.pkl')
    y_pred = gnb.predict(x_test)

    print 'Accuracy :{}'.format(metrics.accuracy_score(y_test, y_pred))
    print metrics.confusion_matrix(y_test, y_pred)


def main():
    method1()


if __name__ == '__main__':
    main()
