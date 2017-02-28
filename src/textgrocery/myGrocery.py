# -*- coding:utf-8 -*-
#
#        Author : TangHanYi
#        E-mail : thydeyx@163.com
#   Create Date : 2017-01-04 06:01:18 CST
# Last modified : 2017-02-17 03:26:22 CST
#     File Name : tgrocery.py
#          Desc :
import sys
import json
from tgrocery import Grocery
import numpy as np

class Solution:
    
    def __init__(self):
        self.grocery = Grocery("sample")
        self.input = open("../data/train_raw.json", "r")

    def get_train_test(self):
        
        info_list = []
        n = 0
        train_set_file = open("train_file.json", "w")
        test_set_file = open("test_file.json", "w")
        for line in self.input:
            n += 1
            info_dict = json.loads(line.strip())
            label = info_dict['label']
            info = info_dict['title']
            url = info_dict['url']
            content = info_dict['content']
            info_list.append((label, info, url, content))
        
        num_array = np.random.permutation(n)
        info_array = np.array(info_list)
        
        n = len(info_array)
        train_set = info_array[num_array][:int(n * 0.7)]
        test_set = info_array[num_array][int(n * 0.7):]
        out_dict = {}
        for label, info, url, content in train_set:
            out_dict['url'] = url
            out_dict['label'] = label
            out_dict['info'] = info
            out_dict['content'] = content
            print >> train_set_file, json.dumps(out_dict)

        out_dict = {}
        for label, info, url, content in test_set:
            out_dict['url'] = url
            out_dict['label'] = label
            out_dict['info'] = info
            out_dict['content'] = content
            print >> test_set_file, json.dumps(out_dict)

        train_set_file.close()
        test_set_file.close()


    def train(self):

        #train_file = open("train_file.json", "r")
        #test_file = open("test_file.json", "r")
        train_file = open("../THUCTC/train_7_3.json", "r")
        test_file = open("../THUCTC/test_7_3.json", "r")
        train_src = []
        test_src = []
        for line in train_file:
            in_dict = json.loads(line.strip())
            try:
                #train_src.append((in_dict['label'], in_dict['info']+" "+in_dict['url'].strip().split("/")[-2]))
                train_src.append((in_dict['label'], in_dict['title']))
            except Exception as e:
                pass

        self.grocery.train(train_src)
        for line in test_file:
            in_dict = json.loads(line.strip())
            try:
                #test_src.append((in_dict['label'], in_dict['info']+" "+in_dict['url'].strip().split("/")[-2]))
                test_src.append((in_dict['label'], in_dict['title']))
            except Exception as e:
                pass
        print len(train_src)
        self.grocery.save()
        print self.grocery.test(test_src)

        """
        k = 0
        tmp = open("tmp", "w")
        for label, info in test_src:
            print >> tmp, self.grocery.predict(info), label
            if str(self.grocery.predict(info)) == label:
                k += 1
        print k*1.0 / len(test_src)
        """


if __name__ == "__main__":
    s = Solution()
    #s.get_train_test()
    s.train() 
