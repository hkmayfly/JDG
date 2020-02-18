# -*- coding=utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
# from splinter.browser import Browser
from JDBuy import *
import sys

Info = ''

mailto_lists = [
    "hkmayfly@vip.qq.com",
    "xxxxxxxx@qq.com",
]  # 收件人邮箱
mail_server = "smtp.qq.com"
mail_sender = "发件人邮箱"  # 发件人地址
mail_pass = "授权码"  # 授权码


# def login():
#     executable_path = {'executable_path': 'D:\Chromedriver\chromedriver.exe'}
#     # browser = Browser("chrome", **executable_path)
#     b = Browser("chrome", **executable_path)
#     b.visit("https://item.jd.com/1842790.html")
#     time.sleep(1)
#     b.click_link_by_text("你好，请登录")
#     time.sleep(1)
#     b.click_link_by_text("账户登录")
#     time.sleep(1)
#     b.fill("loginname","京东账户")
#     time.sleep(1)
#     b.fill("nloginpwd","京东密码")
#     time.sleep(1)
#     b.find_by_id("loginsubmit").click()
#     time.sleep(2)
#     b.click_link_by_text("加入购物车")


def send_mail(mailto_list):
    # 邮件内容，HTML格式
    msg = MIMEText("<p>有货了！点击跳转：<a href=\"%s\">%s</a></p>" % (Info, Info), 'html', 'utf-8')
    # 寄件人，收件人，标题
    msg['From'] = Header('口罩有货了！')
    msg['To'] = Header(mailto_list)
    msg['Subject'] = Header('口罩有货了！')

    try:
    	 # 连接QQ邮箱的SMTP服务
        server = smtplib.SMTP_SSL(mail_server)
        server.connect(mail_server, 465)
        server.login(mail_sender, mail_pass)
        server.sendmail(mail_sender, [mailto_list], msg.as_string())
        server.quit()
    except Exception as e:
        print (str(e))
    print ('发送成功！')


import requests
import time

jd_url_list = ["获取的链接"]

# 京东实时监控函数
def real_time():
    jd_headers={
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
    }
    global Info
    flag = 1
    while True:
        try:
            if flag == 1:
            	   # 检测Cookie有效性
                validate_cookies()
                # 获取京东账户名
                getUsername()
            # 记录检测次数
            flag += 1
            # 检测列表所有链接
            for url1 in jd_url_list:
                req = requests.get(url1, headers=jd_headers, timeout=10)
                # 提取出商品实际链接
                jd_url = "https://item.jd.com/"+ url1.split('skuId=')[1].split('&')[0]+'.html'
                if req.text.find('无货') > 0:
                    print ('[%s]--无货...'%jd_url)
                else:
                	 # 将信息写到日志文件中
                    logger.info('[%s]--有货!!!'%jd_url)
                    # 购买商品，购买异常则退出
                    if buyMask(url1.split('skuId=')[1].split('&')[0]):
                        sys.exit(1)
                    # Info存储到货的商品链接
                    Info = jd_url
        except Exception as e:
            print (str(e))
        if Info != '':
            # 微信信息
            wx_info = '口罩有货了！点击进入:'+'['+Info+']'+'('+Info+')'
            data = {'text': '口罩有货了', 'desp': wx_info}
            # 在Server酱中绑定微信获取
            requests.post('server酱微信接口', data=data)
            # 对列表中的邮箱发送邮件
            for mailto_list in mailto_lists:
                send_mail(mailto_list)
            Info = ''
        time.sleep(5)
        # 每检测20次，就检查一次cookie的有效性
        if flag % 20 == 0:
            logger.info('校验是否还在登录')
            validate_cookies()

if __name__ == '__main__':
     real_time()
