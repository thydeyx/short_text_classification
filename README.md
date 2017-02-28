# 短文本分类 #

### 1.特征处理 ###
对文本分类首先要讲文本转化为模型可以接收的词向量形式，几种常用的处理方法如下：

*1.1 切词后生成词向量*

使用常用的切词工具，如jieba,thulac等对文本切词，将切词后的词进行词频倒排序，以倒序对词标号，得到词向量。

*1.2 bigram作为特征*

根据对中文文本分类的研究，当特征数达到近1万维的时候，采用分词后的词作为特征还是采用字的bigram作为特征，效果相近。因此如果没有比较靠谱的分词系统，就用分词作为特征，如果没有，用bigram也能实现不坏的效果。

*1.3 word2vec生成词向量*

神经网络概率语言模型是一种新兴的自然语言处理算法，该模型通过学习训练语料获取词向量和概率密度函数，词向量是多维实数向量，向量中包含了自然语言中的语义和语法关系，词向量之间余弦距离的大小代表了词语之间关系的远近，词向量的加减运算则是计算机在"遣词造句"。(项目地址:http://radimrehurek.com/gensim/)

另外，可以对源文本进行一些清洗，如下：

	normalize_text() {
  		tr '[:upper:]' '[:lower:]' | sed -e 's/^/__label__/g' | \
    		sed -e "s/'/ ' /g" -e 's/"//g' -e 's/\./ \. /g' -e 's/<br \/>/ /g' \
        	-e 's/,/ , /g' -e 's/(/ ( /g' -e 's/)/ ) /g' -e 's/\!/ \! /g' \
        	-e 's/\?/ \? /g' -e 's/\;/ /g' -e 's/\:/ /g' -e 's/，/ /g'  -e 's/、/ /g' | tr -s " " | myshuf
	}

*1.4 繁体简体转换*

使用langconv可以对文本进行一些繁体向简体的转换。（项目地址：https://github.com/skydark/nstools/blob/master/zhtools/langconv.py）

	from langconv import *
	Converter('zh-hans').convert(line.decode'utf-8'))
	
### 2.特征选择与权重计算 ###
特征选择的主要方法有：

*2.1 信息增益*

[详细解释](http://www.blogjava.net/zhenandaci/archive/2009/03/24/261701.html)

*2.2 开方检验*

[详细解释](http://www.blogjava.net/zhenandaci/archive/2008/08/31/225966.html)

权重计算主要使用tf-idf。

### 3.模型选择 ###

主要对比三中现有文本分类开源项目的效果：

*3.1 TextGrocery*

[TextGrocery] [id]是一个基于LibLinear和结巴分词的短文本分类工具，特点是高效易用，同时支持中文和英文语料。基本无需对特征与模型进行调整，使用简单。

[id]: https://github.com/2shou/TextGrocery  "Optional Title Here"

*3.2 THUCTC*

[THUCTC](http://thuctc.thunlp.org/#%E4%B8%AD%E6%96%87%E6%96%87%E6%9C%AC%E5%88%86%E7%B1%BB%E6%95%B0%E6%8D%AE%E9%9B%86THUCNews)(THU Chinese Text Classification)是由清华大学自然语言处理实验室推出的中文文本分类工具包，能够自动高效地实现用户自定义的文本分类语料的训练、评测、分类功能。文本文类通常包括特征选取、特征降维、分类模型学习三个步骤。如何选取合适的文本特征并进行降维，是中文文本分类的挑战性问题。我组根据多年在中文文本分类的研究经验，在THUCTC中选取二字串bigram作为特征单元，特征降维方法为Chi-square，权重计算方法为tfidf，分类模型使用的是LibSVM或LibLinear。THUCTC对于开放领域的长文本具有良好的普适性，不依赖于任何中文分词工具的性能，具有准确率高、测试速度快的优点。

*3.3 fastText*

[fastText](https://pypi.python.org/pypi/fasttext/)是一个可以有效的学习词的表示形式和对语句进行分类的的工具。

## 3.4 方法对比 ##

通过多次实验，选出如下表几种比较有代表性的实验结果展示。选用的同一套训练测试集得到。

| 工具           |准确率            | 召回率  | 参数      | 特征 | 说明|时间(在下章节中给出的数据集上)|
| ------------- |:--------------:|:-----:|:-----------:|:-----:|:-----:||:-----:|
| TextGrocery   | 0.910495090016 |                | 默认参数                 | 仅切词 | 效率较高，使用简单，既拿即用|5分钟以内|
| THUCTC        | 0.907914397102 | 0.900289382325 | -f 400000 -svm liblinear| 使用bigram |效率较高，切词效果对模型无影响，去停止词可以提生效果|5分钟以内|
| THUCTC        | 0.930124352184 | 0.923914281645 | -f 400000 -svm liblinear| 使用bigram |训练时间很长，预测精度相对于线性模型有提升，-f 参数设置特征维度，高纬度明显提升训练时间和小幅度提高预测精度|3个小时左右|
| fastText      | 0.923842279818 | 0.923842279818 | ws=9, word_ngrams=1, epoch=35| 使用词向量 | 训练速度快，预测精度相对较高，训练轮数增长可以小幅度提高，预测精度|3分钟以内|
| fastText      | 0.984          | 0.984          | 默认参数 | 使用词向量 | 训练速度快，预测精度很高，对英文wiki数据进行的分类|3分钟以内|

通过实验数据表明THUCTC的短文本分类效果最好，但是训练时间远远高于其它模型；fastText分类精度较好，训练速度很快，使用简单，对英文的预测准确精度很高。

### 4.数据收集 ###

实验数据主要由两部分构成：

*1.已有数据集*

已有数据集从网上已经公开的数据集中获得，本次实验选用的为已标注的wiki数据，训练集有56万，测试集有7W，在./data/train/test_english.csv中。

格式：以逗号分隔。label,title,content

| label | count |
| ----- |:-----:|
|Company|44998|
|EducationalInstitution|45000|
|Artist|45000|
|Athlete|45000|
|OfficeHolder|45000|
|MeanOfTransportation|45000|
|Building|44999|
|NaturalPlace|45000|
|Village|44999|
|Animal|45000|
|Plant|45000|
|Album|44999|
|Film|44999|
|WrittenWork|45000|

*2.抓取数据集*

从今日头条抓取数据集，抓取代码在./src/get_data.py，数据量为97000文本的摘要、标题、标签、网址和相关的信息。共10类，每一类数量在1W左右。

格式：json格式。title:标题, label:类别, abs:摘要

| label | count |
| ----- |:-----:|
|fashion|5584|
|finance|5234|
|entertainment|11384|
|car|10605|
|sports|11130|
|society|10405|
|game|11736|
|tech|16786|
|military|8037|
|history|6858|

### 5.一些相关的处理代码和数据 ###

*1.数据*

	./data/
	
		./train_content_title.json (今日头条部分全文数据)
	
		./train_abs_title.json (今日头条全部摘要，标题，标注数据)
	
		./train_english.csv (wiki英文文本训练数据)
	
		./test_english.csv (wiki中文文本训练数据)

*2.代码脚本*

	./src/
		
		./get_data.py (抓取今日头条，正更改为每日定时抓取)
		
		./fasttext/ (fasttext的部分实验代码)
		
		./THUCTC/ (THUCTC的部分实验代码)
		
		./textgrocery/ (textgrocery的部分实验代码)
		
		./othersModel/ (其它模型与特征处理的部分实验代码)
		
		./LSTM/ (神经网络相关的部分实验代码，目前在实验中，需要更多训练数据)