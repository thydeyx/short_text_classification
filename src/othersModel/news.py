# -*- coding:utf-8 -*-
#
#        Author : TangHanYi
#        E-mail : thydeyx@163.com
#   Create Date : 2017-02-21 11:10:25 CST
# Last modified : 2017-02-22 02:55:04 CST
#     File Name : news.py
#          Desc :

from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import SGDClassifier
from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfTransformer
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import json
import numpy as np
import jieba

def download():

    news = fetch_20newsgroups(subset='all')
    print type(news)
    data = news.data
    target = news.target
    n = len(data)
    d = {}
    outf = open('news', 'w')
    for i in range(n):
        d['text'] = data[i]
        d['target'] = target[i]
        out = json.dumps(d)
        print >> outf, out

def train_test():

    #news = fetch_20newsgroups(subset='all')
    inp = open('./data/train1.tsv', 'r')
    k = 0
    data = []
    target = []
    for line in inp:
        line = line.strip()
        ind = json.loads(line)
        text = ind['text']
        #cut_text = ' '.join(list(jieba.cut(text)))
        label = ind['label']
        data.append(text)
        target.append(label)
        k += 1

    data = np.array(data)
    target = np.array(target)
    count_vec = CountVectorizer()
    x_count_data = count_vec.fit_transform(data)
    tf_transformer = TfidfTransformer(use_idf=False).fit(x_count_data)
    x_tfidf = tf_transformer.transform(x_count_data)
    x_count_train, x_count_test, y_train, y_test = train_test_split(x_tfidf, target, test_size=0.3, random_state=33)
    #count_vec = CountVectorizer()
    #x_count_train = count_vec.fit_transform(x_train)
    #x_count_test = count_vec.transform(x_test)
    #x_tfidf_train = TfidfTransformer(use_idf=True).fit(x_count_train)
    #x_tfidf_test = TfidfTransformer(use_idf=True).fit(x_count_test)
    #mnb = MultinomialNB()
    #mnb.fit(x_count_train, y_train)
    #y_true_test = mnb.predict(x_count_test)
    #print mnb.score(x_count_test, y_test)

    #clf = linear_model.LogisticRegression(C=1.0, penalty='l2', tol=1e-6)
    #clf.fit(x_count_train, y_train)
    #y_true_test = clf.predict(x_count_test)
    #print clf.score(x_count_test, y_test)

    #clf = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=50, random_state=42)
    #clf = svm.SVC(decision_function_shape='ovo')
    clf = svm.LinearSVC()
    clf.fit(x_count_train, y_train)
    y_true_test = clf.predict(x_count_test)
    print clf.score(x_count_test, y_test)
    print classification_report(y_true_test, y_test)
    

def test():

    news = fetch_20newsgroups(subset='all')
    print news.target_names

def train_test_wiki():
    inp = open('./data/train.csv', 'r')
    k = 0
    data = []
    target = []
    for line in inp:
        line = line.strip()
        items = line.split(',')
        if len(items) != 3:
            continue
        data.append(items[2].strip())
        target.append(items[0].strip())
        k += 1

    x_train = np.array(data)
    y_train = np.array(target)
    #x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.25, random_state=33)
    inp_test = open('./data/test.csv', 'r')
    k = 0
    data = []
    target = []
    for line in inp_test:
        line = line.strip()
        items = line.split(',')
        if len(items) != 3:
            continue
        data.append(items[2].strip())
        target.append(items[0].strip())
        k += 1
    x_test = np.array(data)
    y_test = np.array(target)
        
    count_vec = CountVectorizer()
    x_count_train = count_vec.fit_transform(x_train)
    x_count_test = count_vec.transform(x_test)
    clf = RandomForestClassifier(n_estimators=10)
    clf.fit(x_count_train, y_train)
    print clf.score(x_count_test, y_test)
    #mnb = MultinomialNB()
    #mnb.fit(x_count_train, y_train)
    #print mnb.score(x_count_test, y_test)

def train_test_gram():

    inp = open('./data/train1.tsv', 'r')
    k = 0
    data = []
    target = []
    for line in inp:
        line = line.strip()
        ind = json.loads(line)
        text = ind['text']
        #cut_text = ' '.join(list(jieba.cut(text)))
        #text = re.sub("：“”:：！，；「『【{《》}】』」·[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), " ".decode("utf8"), text)
        label = ind['label']
        data.append(text)
        target.append(label)
        k += 1

    data = np.array(data)
    target = np.array(target)
    count_vec = CountVectorizer(analyzer='word', ngram_range=(1, 4))
    x_count_data = count_vec.fit_transform(data)
    tf_transformer = TfidfTransformer(use_idf=False).fit(x_count_data)
    x_tfidf = tf_transformer.transform(x_count_data)
    x_count_train, x_count_test, y_train, y_test = train_test_split(x_tfidf, target, test_size=0.3, random_state=33)
    clf = svm.LinearSVC()
    clf.fit(x_count_train, y_train)
    y_true_test = clf.predict(x_count_test)
    print clf.score(x_count_test, y_test)
    print classification_report(y_true_test, y_test)


def look():
    
    inp = open('./data/train1.tsv', 'r')
    for line in inp:
        line = line.strip()
        ind = json.loads(line)
        text = ind['text']
        label = ind['label']
        if label == 'society':
            print text + "\t" + label
        
if __name__ == "__main__":
    #test()
    #train_test_gram()
    #train_test_wiki()
    look()
