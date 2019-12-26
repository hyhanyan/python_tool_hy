#encoding=utf-8;
# 查询域名证书到期情况

import re
import time
import commands
from datetime import datetime
import sys
import json 
import smtplib
from email.mime.text import MIMEText
from email.header import Header

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

def sendMail(body, to, reces):
    sender = 'server-domian@ssp.com'
    #receivers = ['hanyan3@qq.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    receivers = reces  	

    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = "ssp-server"   # 发送者
    message['To'] = to     # 接收者
 
    subject = '域名过期时间提醒'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

def getDomainTime(domain):
    comm = "curl -Ivs https://" + domain + " --connect-timeout 10" 
    result = commands.getoutput(comm)
    #print result

    m = re.search('start date: (.*?)\n.*?expire date: (.*?)\n.*?common name: (.*?)\n.*?issuer: CN=(.*?)\n', result, re.S)
    start_date = m.group(1)
    expire_date = m.group(2)
    common_name = m.group(3)
    issuer = m.group(4)

    # time 字符串转时间数组
    start_date = time.strptime(start_date, "%b %d %H:%M:%S %Y GMT")
    start_date_st = time.strftime("%Y-%m-%d %H:%M:%S", start_date)
    # datetime 字符串转时间数组
    expire_date = datetime.strptime(expire_date, "%b %d %H:%M:%S %Y GMT")
    expire_date_st = datetime.strftime(expire_date,"%Y-%m-%d %H:%M:%S")

    # 剩余天数
    remaining = (expire_date-datetime.now()).days
    print(datetime.now())
    #print ("域名:", domain)
    #print ('通用名:', common_name)
    #print ('开始时间:', start_date_st)
    #print ('到期时间:', expire_date_st)
    #print (remaining)
    #print ('颁发机构:', issuer)
    #print ('*'*30)
    #time.sleep(0.5)
    return remaining, expire_date_st

if __name__ == "__main__":
    data = ""
    to = ""
    receivers = []
    with open('dmail.json', 'r') as f:
    	#data = f.read().decode(encoding='gbk').encode(encoding='utf-8')
    	data = f.read()
    Dinfo = json.loads(data, encoding='utf-8')
    domains = Dinfo["domain"]
    for k,v in Dinfo["mail"].items():
	to = to + k + ","
        receivers.append(v)
    to = to[:-1]
    to = to.encode('utf-8')	
    #exit()
    dictInfo = {} 
    for domain in domains:
        remain, expire = getDomainTime(domain)
        if remain <= 7 :
            dictInfo[domain] = "还有 " + str(remain) + " 天过期，" + " 过期时间为 " + expire 
    if len(dictInfo) > 0:
    	j = json.dumps(dictInfo, ensure_ascii=False, indent=6) 
        sendMail(j, to, receivers)
    #print len(dictInfo)
