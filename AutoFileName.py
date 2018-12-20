#检查目录重命名文件,如果文件filename存在,则自动重命名文件
import os
def Auto_Rename(filename,fold_direction= ".\output\\\\"):
    n=1
    fileExtension = filename.split('.')[1]
    name_temp = filename.split('.')[0:-1]
    filename = fold_direction + filename
    while os.path.isfile(filename):
        filename = fold_direction + ''.join(name_temp) + '_' + str(n)+ '.' + fileExtension
        n +=1
##    print(n)
    print('文件已存在,重命名为{}.'.format(filename))
    return filename
# filenames('001.txt','E:\\PY\\EECS_6201')
# dataFileName = Auto_Rename('scoreDict.csv')

def CSV_to_List(filename):
#获取monthscore矩阵
    print('读取{}文件数据,转为二位数据列表.'.format(filename))
    month_score_list=[]
    list1=[]
    fo = open(filename,'r',encoding = 'utf-8')
    for line in fo:
        line = line.split(',')
        list1.append(line)
    fo.close()
    for item in list1[1:]:
        numbers = list(map(int, item[1:-1]))
        numbers.insert(0,item[0])
        month_score_list.append(numbers)
##    print(month_score_list)
    print('读取完毕!')
    fo.close()
    return month_score_list
##CSV_to_List('new 2.txt')
