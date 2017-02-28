# -*- coding:utf-8 -*-
#
#        Author : TangHanYi
#        E-mail : thydeyx@163.com
#   Create Date : 2017-02-17 03:35:05 CST
# Last modified : 2017-02-17 06:10:08 CST
#     File Name : train.py
#          Desc :
import fasttext

def train():
    #classifier = fasttext.supervised("./data_jrtt/dbpedia.train", "jrtt_news.model", label_prefix="__label__", ws=11, word_ngrams=1, epoch=20)
    #result = classifier.test("./data_jrtt/dbpedia.test")
    classifier = fasttext.supervised("./data_jrtt/train.csv", "jrtt_news.model", label_prefix="__label__", ws=9, word_ngrams=2, epoch=20)
    result = classifier.test("./data_jrtt/test.csv")
    print result.precision
    print result.recall

if __name__ == "__main__":
    train()

