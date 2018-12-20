##GetSyriaNewsScoer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
##from nltk.tokenize import sent_tokenize
import nltk.stem
from nltk import *
import time
import numpy as np
from nltk_rake_test import rake_text
from  AutoFileName import Auto_Rename
from  AutoFileName import CSV_to_List
from  AutoFileName import process_bar
##from  AutoFileName import coeffientArry
##from nltk.stem import WordNetLemmatizer
##from nltk.corpus import treebank
##from nltk.tag import StanfordNERTagger
def saveAsCSV(listToSave,filename,firstLine='Date,Violence_Score,Relief_Score,Enviroment_Score'):
    filename = Auto_Rename(filename)
    fo = open(filename,'w+',encoding = 'utf-8')
##    fo.writelines(firstLine)
    for item in listToSave:
        fo.writelines(str(item))
    fo.close()
    print('存储到  "{}"  文件.'.format(os.path.join(filename)))

def readKeyWords():
    import os
    print("Call readKeyWords() ...\nReading keywords form '\data\' folder")
    fo = open(".\data\ViolenceWordslist.txt")
    violence_seed_words = fo.read().split('\n')
    fo.close()
    fo =  open(".\data\ReliefWords.txt")
    rlf_seed_words= fo.read().split('\n')
    fo.close()
    fo =  open(".\data\EnviromentWordslist.txt")
    enTh_seed_words= fo.read().split('\n')
    fo.close()
    fo =  open(".\data\ReliefWords1.txt")
    relief_words_1= fo.read().split('\n')
    fo.close()
    fo =  open(".\data\ReliefWords2.txt")
    relief_words_2= fo.read().split('\n')
    fo.close()
    return violence_seed_words,rlf_seed_words,enTh_seed_words,relief_words_1,relief_words_2
    print("readKeyWords() Finished...")

def dict_format(time_string):  #dict_format Mar 月份 转换成数字月份 03
    t1 = time.strptime(time_string,'%d %b %Y')
##    print(t1)
    time_string = time.strftime('%Y.%m.%d',t1)
##    print(time_string)
    return time_string

def getNewsScore(fold_direction,SyriaCity):  #给叙利亚新闻打分
##    start_time = time.perf_counter()
    print ('Call newsScoe() start......')
    ScoreListCollection = []
    sub_list =[]
    All_list = []
    N_all_files,N =0,0

    keywordslist = readKeyWords()
    violence_seed_words =keywordslist[0]
    rlf_seed_words=keywordslist[1]
    enTh_seed_words=keywordslist[2]
    relief_words_1=keywordslist[3]
    relief_words_2=keywordslist[4]
##    print(violence_seed_words)
    firstLine = 'Date,Violence_Score,Relief_Score,Enviroment_Score,Key_words\n'
    st = nltk.stem.SnowballStemmer('english')
    stop_words = set(stopwords.words('english'))
##    print( '\nThere is {} stop words in this collection.' .format(len(stop_words)))
    filename = Auto_Rename('scoreDict.csv')
    fo = open(filename,'w+',encoding = 'UTF-8')
    fo.writelines(firstLine)

#遍历文件夹内文件,删选目标区域文件,根据关键词打分
    for root,dirs,files in os.walk(fold_direction):
        files_sum = len(files)
        print('{} files need to be processed...'.format(files_sum))
        for file in files:
            N_all_files +=1
            file = os.path.join(root,file)

            filtered_words =[]
            key_words =[]
            violence_score, relief_score, enviro_score, = 0,0,0
            ScoreDict = {'date':"",'violence_score':"",'relief_score':"",'enviro_score':"", 'key_words':""}
            start_time = time.perf_counter()

            xmlRead = readXML (file)
            date = xmlRead[0]
            # print(date)
            date = dict_format(date)
            txt= xmlRead[3]
            extracted_phrases = rake_text(txt,2,2)
##            print(txt)
##            print(extracted_phrases)
##            print(txt[:5])
            word_tokens = word_tokenize(txt)
            filtered_words = [w for w in word_tokens if w not in stop_words and w.isalpha()]
            filtered_words = [st.stem(w) for w in filtered_words]
##            print(filtered_words[:9])
            tagged_words = nltk.pos_tag(filtered_words)
##            print(tagged_words[:9])
            regex = 'NN.*|V.*|RB.*'
            filterTagged_words = [w for w in tagged_words if re.search(regex,w[1])]
            filterTagged_words2 = []
            for item in filterTagged_words:
                filterTagged_words2.append(item[0])
            filterTagged_words = []
            filterTagged_words = filterTagged_words2 + extracted_phrases #合并文章提取的关键词和关键词组
##            print(filterTagged_words)
            if SyriaNewsOrNot(SyriaCity,filtered_words):
                N +=1
                for w in filterTagged_words:
                    if w in violence_seed_words:
                        violence_score +=1
                        key_words.append(w)
##                        print(item)
                    elif w in relief_words_2:
                        relief_score +=2
                        key_words.append(w)
##                        print(item)
                    elif w in relief_words_1:
                        relief_score +=1
                        key_words.append(w)
##                        print(item)
                    elif w in enTh_seed_words:
                        enviro_score +=1
                        key_words.append(w)
##                        print(item)
                    Score_sum = violence_score + relief_score + enviro_score

##                ScoreDict['date'],ScoreDict['violence_score'],ScoreDict['relief_score'],ScoreDict['enviro_score'],ScoreDict['Score_Sum'],ScoreDict['key_words_list'] =\
##                                                                                                                                                date,violence_score,relief_score,enviro_score,Score_sum,key_words
                sub_list =[date,violence_score,relief_score,enviro_score,Score_sum,str(' '.join(key_words))]
                All_list.append(sub_list)
##                ScoreListCollection.append(ScoreDict)
                # print('File No. :==={0}/{2}===, File direction&name : {1}  ' .format( str(N),str(file),str(N_all_files)))
##                print("{0:=^20},{1:>5},{2:>5},{3:>5},{4:>5}".format(date,violence_score,relief_score,enviro_score,Score_sum))

                ScoreListString = date+","+str(violence_score)+","+str(relief_score)+","+str(enviro_score)+","+' '.join(key_words)+'\n'

                fo.writelines(ScoreListString) #输出一个文本文件,下一步处理使用
            # else:
                # print('********Not Syria Related News*********')
##                print('File No. :==={0}/{2}===, File direction&name : {1}  ' .format( str(N),str(file),str(N_all_files)))
            if N_all_files ==1 or N_all_files%1000==0:
                dur = time.perf_counter() - process_strat
                process_bar(N_all_files,files_sum,20,dur)
##            fodict = open('ScoreListCollection.txt','w+',encoding = 'UTF-8')
##            fodict.write(str(ScoreListCollection))#输出一个字典文件,后续使用
##            fodict.close()
    fo.close()
    print('Score Extacting Finished!')
##    print(All_list[:4])
    return All_list, filename

def readXML(filename): # 提取xml文件中的内容,返回tuple
    import xml.etree.ElementTree as ET
    import time
    from nltk import word_tokenize
    import re
    timeStr, sourceName, title , content, phrases = [],[],[],[],[]
    try:
        fo = open(filename,'r+',encoding = 'utf-8')
        text=fo.read()
        text = re.sub('&#[0-9]*;*-*|- |&lt;*-*|-*&gt;*|&amp;*|;', "" ,text)
        fo.close()
##        tree = ET.parse(filename)
##        root = tree.getroot()
##    print('root-tag:',root.tag,',root-attrib:',root.attrib,',root-text:',root.text)
        root=ET.fromstring(text)
        docName = root.find("Id").text
        sourceName = root.find("SourceName").text
        title = root.find("Title").text
        timeStr = root.find("PublicationDateTime").text[:-9]
        content = str(root.find("Content").text)
        phrases = rake_text(content)
        content = word_tokenize(content)
        fo.close()
##        print (phrases)
##    except:
##        print('Error,Not correct content!')
    finally:
        return timeStr, sourceName, title, content, phrases

#验证新闻是不是关于目标地区的新闻,返回True / Flase #参数SyriaCity = 目标地区城市列表'\n'分割的字符串文件, txt = 需要验证的新闻字符串
def SyriaNewsOrNot(SyriaCity,txt):
    for city in SyriaCity:
        for words in txt:
            if words == city:
                return True
                break
        else:
            continue
        break
    return False

def monthScore(All_list): # 所有文件打分按月份重新统计,输出已月份时间为key , 分数值为value 的字典
    print('monthScore() start......')
##    month_org= ['01','02','03','04','05','06','07','08','09','10','11','12']
    month_list =[]
    month_score_list= []
    sub_list = []
    month_score_v , month_score_r ,  month_score_e, month_score_s = 0, 0, 0, 0

    for item in All_list:
        month_list.append(item[0][:7])
    month_list = list(set(month_list))
##    print(month_list)
    for month in month_list:
        for item in All_list:
            if item[0][:7] == month:
                month_score_v += item[1]
                month_score_r +=  item[2]
                month_score_e +=  item[3]
                month_score_s =  month_score_v + month_score_r + month_score_e
        sub_list = [month,month_score_v,month_score_r,month_score_e, month_score_s]
        month_score_list.append(sub_list)
        month_score_v , month_score_r ,  month_score_e, month_score_s = 0, 0, 0, 0
    month_score_list = sorted(month_score_list,key = lambda x: float(eval(x[0]))) #按月份先后排序
##    print(month_score_list[:20])
    print ('Months Scoe() Finished!')
    return month_score_list

def main():
##    import numpy as np
##    month_score_list = []
##    fo = open('.\data\Syria cities name.txt','r',encoding = 'ANSI')
##    SyriaCity = str.lower(fo.read())
##    SyriaCity = SyriaCity.split('\n')
##    fo.close()
####
##    fold_direction = ".\\test_matirial"        #test用数据文件夹
##    fold_direction = "E:\\PY\\NEWS"              #实际工作新闻集
##    ScoreListCollection = getNewsScore(fold_direction,SyriaCity)
##    filename =ScoreListCollection[1] #从新闻读取数据,已读取存入文件,获取文件名
##    print('文章:日期,分数,关键词已写入 {} 文件.'.format(filename))
    filename = 'scoreDict.csv'
    ScoreListCollection=CSV_to_List(filename) #从新闻读取数据,已读取存入文件,不需要再使用
    print('按月份统计各项分数,输出到文件.')
    month_score_list = monthScore(ScoreListCollection)
##    print(month_score_list[:2])
    saveAsCSV(month_score_list,'coeffient_arry.csv')


global process_strat
process_strat = time.perf_counter()
main()
processing_time =  time.perf_counter() - process_strat
print('Total running time is {0:=^10.2f} senconds.'.format(processing_time))
