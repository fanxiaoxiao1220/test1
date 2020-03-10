# coding=utf-8


import csv
import sys
import datetime
import os

base_path = sys.argv[1]
actual_path = sys.argv[2]

formatFiledArr = sys.argv[3].split(',')
precision = sys.argv[4].split(',')
trimFiledArr = sys.argv[5].split(',')
fileType = 'bcdf'
header = []
indexDecimal = []
indexTrim = []
precisionArr = []
precision_str = '%.{p}f'
IndexAlready = False


def formatFiled(line, indexArr):
    for i, n in zip(indexArr, range(len(indexArr))):
        a = float(line[i])
        line[i] = precisionArr[n] % a


def trimFiled(line, indexTrim):
    for i in indexTrim:
        line[i] = line[i].strip()


def getIndex():
    global IndexAlready
    for i in range(0, len(header)):
        for filed in formatFiledArr:
            if filed == header[i]:
                indexDecimal.append(i)
                print ('filed :%s is %d column will format' % (filed, i))
        for filed in trimFiledArr:
            if filed == header[i]:
                indexTrim.append(i)
                print ('filed :%s is %d column will trim' % (filed, i))
    IndexAlready = True


print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


# trim and format decimal
def format_bcdf_file(path_source, path_sink):
    global header
    filetoread = open(path_source, 'rU')
    filetowrite = open(path_sink, 'wb')
    reader = csv.reader(filetoread)
    writer = csv.writer(filetowrite)
    for line in reader:
        if line[0] == 'h' and IndexAlready == False:
            header = line
            getIndex()
            if len(indexDecimal) < len(formatFiledArr) and formatFiledArr[0] != 'null':
                print ('It has invaild  filed name ,please check input param ')
                sys.exit(1)
            if len(indexTrim) < len(trimFiledArr) and trimFiledArr[0] != 'null':
                print ('It has invaild  filed name ,please check input param ')
                sys.exit(1)
        if line[0] == 'd':
            formatFiled(line, indexDecimal)
            trimFiled(line, indexTrim)

        writer.writerow(line)
    filetowrite.close()
    filetoread.close()


def format_csv_file(path_source, path_sink):
    global header
    filetoread = open(path_source, 'rU')
    filetowrite = open(path_sink, 'wb')
    reader = csv.reader(filetoread)
    writer = csv.writer(filetowrite)
    lineNum = 1
    for line in reader:
        if lineNum == 1 and IndexAlready == False:
            header = line
            getIndex()
            if len(indexDecimal) < len(formatFiledArr) and formatFiledArr[0] != 'null':
                print ('It has invaild  filed name ,please check input param ')
                sys.exit(1)
            if len(indexTrim) < len(trimFiledArr) and trimFiledArr[0] != 'null':
                print ('It has invaild  filed name ,please check input param ')
                sys.exit(1)
        if lineNum != 1:
            formatFiled(line, indexDecimal)
            trimFiled(line, indexTrim)
        lineNum = lineNum + 1
        writer.writerow(line)
    filetowrite.close()
    filetoread.close()


def start_format(file_dir):
    dir_list = os.listdir(file_dir)
    print dir_list
    for cur_file in dir_list:
        # 获取文件的绝对路径
        path_source = os.path.join(file_dir, cur_file)
        path_sink = os.path.join(file_dir, 'format_file/')
        if not os.path.exists(path_sink):
            os.mkdir(path_sink)

        if os.path.isfile(path_source):
            if not os.path.exists(path_sink):
                os.mkdir(path_sink)
            path_sink = os.path.join(file_dir, 'format_file', cur_file)
            print path_source, "===format_file===", path_sink
            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'start format file %s' % cur_file
            if fileType == 'bcdf':
                format_bcdf_file(path_source, path_sink)
            else:
                format_csv_file(path_source, path_sink)
            print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'end format file %s' % cur_file


def init_format():
    for i in precision:
        precisionArr.append(precision_str.format(p=i))
    print precisionArr
    global base_path, actual_path
    start_format(base_path)
    start_format(actual_path)
    base_path = os.path.join(base_path, 'format_file/')
    base_path = os.path.join(actual_path, 'format_file/')


init_format()

print datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
