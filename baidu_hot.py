# _*_ coding:utf-8 _*_
# author: huage
# 需求：定时获取百度热词并发送邮件
# 开发工具: PyCharm CE
# 开发时间: 2021/8/31 10:05 AM
# 待完善：

'''
说明：修改server、sender、pwd、receivers即可使用
'''

'''
更新日志
2021/9/14
1.使用html格式发送正文

'''

import requests
import datetime
from lxml import etree
import smtplib
from email.mime.text import MIMEText

#发送邮件函数
def send_email(body):
    #---设置参数---
    #实例化SMTP对象，设置SMTP服务器地址
    server = smtplib.SMTP_SSL('smtp.163.com')
    #设置发件人邮箱
    sender = 'XXX@163.com'
    #设置发件人邮箱授权码
    pwd = 'fjadsfdsaof'

    #多个收件人
    receivers = ['hello@outlook.com', 'hello@qq.com']

    #---构造邮件内容---
    subject = '百度热搜榜'
    content = body

    #纯文本邮件
    #message = MIMEText(content,'plain','utf-8')

    #html格式邮件
    message = MIMEText(content,'html','utf-8')
    message['From'] = sender
    message['To'] = ', '.join(receivers)
    message['subject'] = subject

    #登录并发送邮件
    server.login(sender,pwd)
    try:
        server.sendmail(from_addr=sender,to_addrs=receivers,msg=message.as_string())
        #关闭STMP对象
        server.quit()
        print('发送成功')
    except:
        print('发送失败')

#获取内容函数
def get_page(url):
    try:
        user_agent={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
        r=requests.get(url=url,headers=user_agent)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return "发生错误"

#解析内容函数
def parse_page(page):
    page_tree = etree.HTML(page)
    # 直接定位相同xpath路径，以列表形式获得所有内容
    title = page_tree.xpath('//div[@class = "c-single-text-ellipsis"]/text()')

    # 获取热点内容网址
    title_url = page_tree.xpath('//div[@class = "category-wrap_iQLoo horizontal_1eKyQ"]/a/@href')

    content = ''
    for i in range(20):
        # html中通过标签 <a> 来定义链接
        news = '{}.<a href="{}">{}</a>'.format(i + 1, title_url[i], title[i])
        content = content + ' <br> ' + news + ' <br> '
        #print(content)

    return content


if __name__ == '__main__':
    url = 'https://top.baidu.com/board?tab=realtime'

    now = datetime.datetime.now()
    time_str = now.strftime("%m/%d %H:%M")

    content = parse_page(get_page(url))
    body = """
    <html>
    <h1>百度热搜榜</h1>
    <p>
    Hello，华哥！<br>
    这是今天的即时百度热搜榜，请您查收。
    <br>&nbsp;&nbsp;&nbsp;&nbsp;
    {}
    <hr>
    Best Regards<br>

    {}
    </p>
    </html>
    """.format(content,time_str)

    send_email(body)



