#codeing-utf-8

import string,sys
import json

def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

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
    fileresult = filename + '.result'
    fp = open(filename,'r')

    try:
        lines = fp.readlines()
    finally:
        fp.close()

    fw = open(fileresult,'w')
    rows = 24
    cols = 6
    arr_Recog_cost_sum = genMatrix(rows,cols)
    arr_Recog_cost_num = genMatrix(rows,cols)
    
    arr_Recog_wait_sum = genMatrix(rows,cols)
    arr_Recog_wait_num = genMatrix(rows,cols)
    
    arr_Wc_wait_sum = genMatrix(rows,cols)
    arr_Wc_num = genMatrix(rows,cols)
    
    arr_Nlu_wait_sum = genMatrix(rows,cols)
    arr_Nlu_num = genMatrix(rows,cols)
    
    arr_snum = genMatrix(rows,cols)
    arr_num = genMatrix(rows,cols)
    
    for line in lines:
        arr_tmp = line.strip().split()
        if len(arr_tmp) < 3:
            continue
        hours = int(arr_tmp[0])
        minutes = getMinutes(int(arr_tmp[1]))
        err_no = int(arr_tmp[3])
        arr_snum[hours][minutes] += 1
        if len(arr_tmp) < 8:
            continue
        elif len(arr_tmp) == 8:
            Recog_timecost = int(arr_tmp[4])

            Recog_waitfish = int(arr_tmp[5])
            
            Wc_timecost = int(arr_tmp[6])

            Nlu_timecost = int(arr_tmp[7])
        
            if err_no == 0:
                arr_num[hours][minutes] += 1

                if Recog_timecost != 0:
                    arr_Recog_cost_num[hours][minutes] += 1
                    arr_Recog_cost_sum[hours][minutes] += Recog_timecost
    
                if Recog_waitfish != 0:
                    arr_Recog_wait_num[hours][minutes] += 1
                    arr_Recog_wait_sum[hours][minutes] += Recog_waitfish

                if Wc_timecost != 0:
                    arr_Wc_wait_sum[hours][minutes] += Wc_timecost
                    arr_Wc_num[hours][minutes] += 1

                if Nlu_timecost != 0:
                    arr_Nlu_wait_sum[hours][minutes] += Nlu_timecost
                    arr_Nlu_num[hours][minutes] += 1
    
    for i in range(rows):
        for j in range(cols):
            if arr_snum[i][j] != 0 and arr_num[i][j] != 0 and arr_Recog_cost_num != 0 and arr_Recog_wait_num != 0 and arr_Wc_num[i][j] !=0 and arr_Nlu_num[i][j] != 0:
                percentage = format(float(arr_num[i][j])/float(arr_snum[i][j]),'.4f')
                recog_aver_cost = format(float(arr_Recog_cost_sum[i][j])/float(arr_Recog_cost_num[i][j]),'.4f')
                recog_aver_wait = format(float(arr_Recog_wait_sum[i][j])/float(arr_Recog_wait_num[i][j]),'.4f')
                wc_aver_wait = format(float(arr_Wc_wait_sum[i][j])/float(arr_Wc_num[i][j]),'.4f')
                nlu_aver_wait = format(float(arr_Nlu_wait_sum[i][j])/float(arr_Nlu_num[i][j]),'.4f')
                str_tt = str(i) + "H" + str(j) + "M" + " " + str(percentage) + " " + str(recog_aver_cost) + " " + str(recog_aver_wait)
                str_tt = str_tt + " " + str(wc_aver_wait) + " " + str(nlu_aver_wait)
                str_tt = str_tt + " " + str(arr_snum[i][j]) + "\n"
                #print(str_tt)
                fw.write(str_tt)
    fp.close()
    fw.close()


if __name__ == '__main__':
    filename = 'proxy_finally_hy.txt'
    filename = 'test.txt'
    #filename = 'end.txt'
    filename = 'end_ts_ex_0730_597.txt'
    
    Readfile(filename)
