# -*- coding:utf-8 -*-
#
#        Author : TangHanYi
#        E-mail : thydeyx@163.com
#   Create Date : 2017-01-06 01:33:36 CST
# Last modified : 2017-02-20 03:59:32 CST
#     File Name : process.py
#          Desc :

import json
import os
import sys
import numpy
from sklearn import cross_validation

def TrainTest():
    c = []
    inp = open('../data/train.json', 'r')
    out_train = open(r'./train_7_3.json', 'w')
    out_test = open(r'./test_7_3.json', 'w')
    for line in inp:
        line = line.strip()
        c.append(line)
    c_train, c_test = cross_validation.train_test_split(c, test_size=0.3)
    for i in c_train:
        print >> out_train, i
    for i in c_test:
        print >> out_test, i

def genTrianTest():
    inp = open('./test_9_1.json', 'r')
    class_dict = {}
    for line in inp:
        line = line.strip()
        in_dict = json.loads(line)
        label = in_dict['label']
        content = in_dict['abs']
        if len(content) < 5:
            continue
        if class_dict.has_key(label):
            class_dict[label] += 1
        else:
            class_dict[label] = 1
            command = 'mkdir -p ./Train_abs/' + label
            os.system(command)
        out_file = open('./Train_abs/' + label + "/" + str(class_dict[label]) + ".txt", "w")
        print >> out_file, content.encode('utf-8')


if __name__ == "__main__":
    #TrainTest()
    genTrianTest()
