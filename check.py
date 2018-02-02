# coding:utf-8
# author: WenR0

from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from utils import load_php_opcode, recursion_load_php_file_opcode
import sys



if __name__ == '__main__':
    php_file_name = sys.argv[1]
    print 'Checking the file {}'.format(php_file_name)

    # 之前的数据
    white_file_list = []
    black_file_list = []

    with open('black_opcodes.txt', 'r') as f:
        for line in f:
            black_file_list.append(line.strip('\n'))

    with open('white_opcodes.txt', 'r') as f:
        for line in f:
            white_file_list.append(line.strip('\n'))

    all_token = []
    all_token = white_file_list + black_file_list

    # 准备数据
    token = load_php_opcode(php_file_name)
    all_token.append(token)
    X = all_token

    # CV 处理
    cv = CountVectorizer(ngram_range=(3, 3), decode_error="ignore", token_pattern=r'\b\w+\b', min_df=1, max_df=1.0)
    X = cv.fit_transform(X).toarray()


    # tf-idf
    transformer = TfidfTransformer(smooth_idf=False)
    x_tfidf = transformer.fit_transform(X)
    X = x_tfidf.toarray()

    # end 准备数据

    gnb = joblib.load('save/gnb.pkl')
    y_p = gnb.predict(X[-1:])
    
    if y_p == [0]:
        print 'Not Webshell'
    elif y_p == [1]:
        print 'Webshell!'
