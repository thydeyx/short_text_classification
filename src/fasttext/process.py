# -*- coding:utf-8 -*-
#
#        Author : TangHanYi
#        E-mail : thydeyx@163.com
#   Create Date : 2017-01-06 01:33:36 CST
# Last modified : 2017-02-17 06:09:25 CST
#     File Name : process.py
#          Desc :

import json
import os
import sys
import jieba
reload(sys)
sys.setdefaultencoding('utf-8')
import thulac

if __name__ == "__main__":
    #inp_train = open('../src/train_file.json','r')
    #inp_test = open('../src/test_file.json','r')
    inp_train = open('../THUCTC/train_7_3.json','r')
    inp_test = open('../THUCTC/test_7_3.json','r')
    outp_train = open('./data_jrtt/train.csv', 'w')
    outp_test = open('./data_jrtt/test.csv', 'w')
    class_dict = {}
    k = 1
    thu1 = thulac.thulac(seg_only=True)
    for line in inp_train:
        line = line.strip()
        in_dict = json.loads(line)
        label = in_dict['label']
        #title = in_dict['info'].strip()
        #content = in_dict['content'].strip()
        title = in_dict['title'].strip()
        content = in_dict['abs'].strip()
        if class_dict.has_key(label) == False:
            class_dict[label] = k
            k += 1
        #print >> outp_train, class_dict[label] , ',"' + title + '","' + content + '"'
        if len(content) < 5 or len(title) < 1:
            continue
        #print >> outp_train, class_dict[label] , ' , "' + ' '.join(list(jieba.cut(title))) + '" , "' + ' '.join(list(jieba.cut(content))) + '"'
        try:
            c = []
            for i in thu1.cut(content):
                c.append(i[0])
            t = []
            for i in thu1.cut(title):
                t.append(i[0])
        except Exception as e:
            continue
        #print >> outp_train, ' '.join(list(jieba.cut(title))) + '\t' + ' '.join(list(jieba.cut(content))) + '\t' + '__label__'+label.strip()
        print >> outp_train, ' '.join(t) + '\t' + ' '.join(c) + '\t' + '__label__'+label.strip()
    outp_train.close()
    for line in inp_test:
        line = line.strip()
        in_dict = json.loads(line)
        label = in_dict['label']
        #title = in_dict['info'].strip()
        #content = in_dict['content'].strip()
        title = in_dict['title'].strip()
        content = in_dict['abs'].strip()
        if class_dict.has_key(label) == False:
            class_dict[label] = k
            k += 1
        if len(content) < 5 or len(title) < 1:
            continue
        #print >> outp_test, class_dict[label] , ',"' + title + '","' + content + '"'
        #print >> outp_test, class_dict[label] , ' , "' + ' '.join(list(jieba.cut(title))) + '" , "' + ' '.join(list(jieba.cut(content))) + '"'
        try:
            c = []
            for i in thu1.cut(content):
                c.append(i[0])
            t = []
            for i in thu1.cut(title):
                t.append(i[0])
        except Exception as e:
            continue
        #print >> outp_test, ' '.join(list(jieba.cut(title))) + '\t' + ' '.join(list(jieba.cut(content))) + '\t' + '__label__'+label.strip()
        print >> outp_test, ' '.join(t) + '\t' + ' '.join(c) + '\t' + '__label__'+label.strip()
        #print >> outp_test, ' '.join(list(jieba.cut(title))) + '\t' + ' '.join(list(jieba.cut(content))) + '\t' + '__label__'+label.strip()
    outp_test.close()
    """
    if class_dict.has_key(label):
        class_dict[label] += 1
    else:
        class_dict[label] = 1
        command = 'mkdir -p ./Train1/' + label
        os.system(command)
    out_file = open('./Train1/' + label + "/" + str(class_dict[label]) + ".txt", "w")
    print >> out_file, content.encode('utf-8')
    """
