#codeing-utf-8

import string,sys
import json

def genMatrix(rows,cols):
    matrix = [[0 for col in range(cols)] for row in range(rows)]  
    return matrix

def printMatrix(matrix,rows,cols):
    for i in range(rows):
        for j in range(cols):
            print matrix[i][j],
        print '\n'  

def getMinutes(minutes):
    return minutes/10

def Readfile(filename):
    fileresult = filename + '.result.sum'
    fp = open(filename,'r')

    try:
        lines = fp.readlines()
    finally:
        fp.close()

    fw = open(fileresult,'w')
    rows = 24
    cols = 6
    arr_sum = genMatrix(rows,cols)
    arr_num = genMatrix(rows,cols)
    arr_snum = genMatrix(rows,cols)
    
    for line in lines:
        arr_tmp = line.strip().split()
        if len(arr_tmp) < 4:
            continue
        elif len(arr_tmp) == 4:
            hours = int(arr_tmp[0])
            minutes = getMinutes(int(arr_tmp[1]))
            err_no = int(arr_tmp[2])
            timecost = int(arr_tmp[3])
        
            arr_snum[hours][minutes] += 1
            if err_no == 0:
                arr_num[hours][minutes] += 1
                arr_sum[hours][minutes] += timecost
    
    for i in range(rows):
        for j in range(cols):
            if arr_snum[i][j] != 0 and arr_num[i][j] != 0:
                percentage = format(float(arr_num[i][j])/float(arr_snum[i][j]),'.4f')
                aver_cost = format(float(arr_sum[i][j])/float(arr_num[i][j]),'.4f')
                str_tt = str(i) + "H" + str(j) + "M" + " " + str(percentage) + " " + str(aver_cost) + " " + str(arr_snum[i][j]) + "\n"
                #str_tt = str(i) + "H" + str(j) + "M" + " " + str(arr_snum[i][j]) + "\n"
                fw.write(str_tt)
    fp.close()
    fw.close()


if __name__ == '__main__':
    filename = 'proxy_finally_hy.txt'
    filename = 'test.txt'
    filename = 'end_ts_ex_792_0730.txt'
    
    Readfile(filename)
