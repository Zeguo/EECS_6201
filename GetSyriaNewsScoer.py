##GetSyriaNewsScoer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
##from nltk.tokenize import sent_tokenize
import nltk.stem
from nltk import *
import time
import numpy as np
from nltk_rake_test import rake_text
##from nltk.stem import WordNetLemmatizer
##from nltk.corpus import treebank
##from nltk.tag import StanfordNERTagger
def dict_format(time_string):
    t1 = time.strptime(time_string,'%d %b %Y')
##    print(t1)
    time_string = time.strftime('%Y.%m.%d',t1)
##    print(time_string)
    return time_string
#给叙利亚新闻打分

def process_bar(done,allJobs,bar_longth=20,prcessign_duration=0):
    a =round(done/allJobs)*bar_longth
    a_str = '*'* a
    b = '-' * (bar_longth-a)
    c = (done/allJobs)*100
    H = round(prcessign_duration//3600)
    M = round((prcessign_duration%1600)//60)
    S = round(prcessign_duration %60)
    time_str = str(H) + 'H : ' +str(M) + 'M : ' +str(S) + 'S'
    print( 'Processing {0:>3.0f}%  [{1}->{2}] {4:>6} files for: {3}'.format(c,a_str,b,time_str,done))

def getNewsScore(fold_direction,SyriaCity):
##    start_time = time.perf_counter()
    print ('Call newsScoe() start......')
    violence_seed_words =[ 'violence', 'conflict', 'fight','fighter','kill','battle', 'massacre','butchery','injury', 'bombing',\
                           'explosion', 'corpse', 'abduction', 'ambush', 'suicide', 'rape', 'persecution','assassination', 'terror',\
                           'military', 'attack','mortar','forc',]
    rlf_seed_words = ['relief', 'disaster', 'emergency situation', 'refugee camp', 'tent', 'aid', 'host community',\
                      'outbreak', 'infectious diseases', 'epidemic', 'disease', 'contagious', 'infection', 'donor',\
                      'vaccination', 'campaign', 'reconstruction', 'supplies', 'medical', 'grant']
    enTh_seed_words = ['natural resources', 'food scarcity', 'food shortage', 'drought, flood',\
                       'environmental degradation', 'countrysid', 'rural', 'agriculture', 'farmer', 'temperature',\
                       'crop production', 'climate chang']
    relief_words_2 = ['effort', 'relief', 'humanitarian', 'emergency', 'organization','infectious diseases', 'agency', 'aid','emergency situation', 'refugee camp', 'donor', 'campaign', 'charity', 'assist','voluntary', 'motivation', 'rebuild', 'establish', 'UNICEF', 'NGO','UN'] 
    relief_words_1 = ['host community','epidemic', 'vaccination', 'nutrition', 'supplies', 'protect', 'shelter', 'cloth', 'food', 'money', 'water']
    
    firstLine = 'Date,Violence_Score,Relief_Score,Enviroment_Score,Key_words\n'

    st = nltk.stem.SnowballStemmer('english')
    items = []
    ScoreListCollection = []
    sub_list =[]
    All_list = []
    stop_words = set(stopwords.words('english'))
    
##    dir="E:\\PY\\NEWS"  #新闻存放文件夹地址
##    print(SyriaCity[:5])
    
##    print(st.stem(' '.join(violence_seed_words)))
##    print(st.stem(' '.join(rlf_seed_words)))
##    print(st.stem(' '.join(enTh_seed_words)))
    
##    print( '\nThere is {} stop words in this collection.' .format(len(stop_words)))
    
    #待筛选文件地址读取
##    fo = open( 'SyriaNewsNameList.txt', 'r', encoding = 'ANSI')
##    file_dir = fo.read()
##    file_dir = file_dir.split('\n')
##    fo.close()
    fo = open('scoreDict.csv','w+',encoding = 'UTF-8')
    fo.writelines(firstLine)
    fo.close()
    N_all_files,N =0,0
    
    for root,dirs,files in os.walk(fold_direction):
        files_sum = len(files)
        print('{} files need to be processed...'.format(files_sum))
        for file in files[:]:
            N_all_files +=1
            file = os.path.join(root,file)
            
            filtered_words =[]
            key_words =[]
            violence_score = 0
            relief_score = 0
            enviro_score = 0
            ScoreDict = {'date':"",'violence_score':"",'relief_score':"",'enviro_score':"", 'key_words':""}
            start_time = time.perf_counter()
            
            xmlRead = readXML (file)
            date = xmlRead[0]
##            print(date)
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
            regex = 'NN.*|V.*|RB'        
            filterTagged_words = [w for w in tagged_words if re.search(regex,w[1])]
            filterTagged_words2 = []
            for item in filterTagged_words:
                filterTagged_words2.append(item[0])
            filterTagged_words = []
            filterTagged_words = filterTagged_words2 + extracted_phrases
##            print(filterTagged_words)
            if SyriaNewsOrNot(SyriaCity,filtered_words):
                N +=1
                for item in filterTagged_words:                    
                    if item in violence_seed_words:
                        violence_score +=1
                        key_words.append(item)
##                        print(item)
                    elif item in relief_words_2:
                        relief_score +=2
                        key_words.append(item)
##                        print(item)
                    elif item in relief_words_1:
                        relief_score +=1
                        key_words.append(item)
##                        print(item)
                    elif item in enTh_seed_words:
                        enviro_score +=1
                        key_words.append(item)
##                        print(item)
                    Score_sum = violence_score + relief_score + enviro_score
                        
##                ScoreDict['date'],ScoreDict['violence_score'],ScoreDict['relief_score'],ScoreDict['enviro_score'],ScoreDict['Score_Sum'],ScoreDict['key_words_list'] =\
##                                                                                                                                                date,violence_score,relief_score,enviro_score,Score_sum,key_words
                sub_list =[date,violence_score,relief_score,enviro_score,Score_sum,str(' '.join(key_words))]
                All_list.append(sub_list)
##                ScoreListCollection.append(ScoreDict)
##                print('File No. :==={0}/{2}===, File direction&name : {1}  ' .format( str(N),str(file),str(N_all_files)))
##                print("{0:=^20},{1:>5},{2:>5},{3:>5},{4:>5}".format(date,violence_score,relief_score,enviro_score,Score_sum))

                ScoreListString = date+","+str(violence_score)+","+str(relief_score)+","+str(enviro_score)+","+' '.join(key_words)+'\n'
                fo = open('scoreDict.csv','a+',encoding = 'UTF-8')
                fo.writelines(ScoreListString) #输出一个文本文件,暂不使用                
##            else:
##                print('********Not Syria Related News*********')
##                print('File No. :==={0}/{2}===, File direction&name : {1}  ' .format( str(N),str(file),str(N_all_files)))
            if N_all_files ==1 or N_all_files%100 ==0:
                dur = time.perf_counter() - process_strat
                process_bar(N_all_files,files_sum,20,dur)           
##            cycle_time = time.perf_counter()-start_time
##            print('此文件处理时间:{0:.2f}秒\n' .format(cycle_time ))
            
##            fodict = open('ScoreListCollection.txt','w+',encoding = 'UTF-8')
##            fodict.write(str(ScoreListCollection))#输出一个字典文件,后续使用
##            fodict.close()
    fo.close()    
##    print(ScireListCollection)
    print('Scoring Finished!')
##    print(All_list)
    return All_list

# 提取xml文件中的内容,返回tuple
def readXML(filename):
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
    
##    file_dir = 'E:\PY\ScoreListCollection.txt'
##    scoreDict =eval( open(file_dir,'r',encoding = 'UTF-8').read())
##    date = scoreDict[0]['date']
##    news_score = int(scoreDict[0]['Score_Sum'])
    
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
                month_score_s+=  item[4]
        sub_list = [month,month_score_v,month_score_r,month_score_e, month_score_s]                 
        month_score_list.append(sub_list)
        month_score_v , month_score_r ,  month_score_e, month_score_s = 0, 0, 0, 0
##    print(month_score_list[:20])
    print ('Months Scoe() Finished!')
    return month_score_list

def main():
    import numpy as np
    np.arr = []
    month_score_list = []
    fo = open('.\data\Syria cities name.txt','r',encoding = 'ANSI')
    SyriaCity = str.lower(fo.read())
    SyriaCity = SyriaCity.split('\n')
    fo.close()

    fold_direction = "E:\\PY\\test_matirial" 
    ScoreListCollection = getNewsScore(fold_direction,SyriaCity)
    month_score_list = monthScore(ScoreListCollection)

    month_score_list = sorted(month_score_list,key = lambda x: float(eval(x[0]))) #按月份先后排序
##    print(month_score_list)

#获取monthscore矩阵
    fo = open('coeffient_arry.txt','w+',encoding = 'utf-8')
    for item in month_score_list:
        np.arr.append(item[1:5])
        fo.writelines(str(item[1:5]))
    print('Month Scores array:\n' )
    fo.close()
    print(np.arr)

global process_strat
process_strat = time.perf_counter()
main()
processing_time =  time.perf_counter() - process_strat
print('Total running time is {0:=^10.2f} senconds.'.format(processing_time))


