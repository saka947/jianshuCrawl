# -*- coding: utf-8 -*
import requests,os,os.path as p
from lxml import etree
import re

postfix='https://www.jianshu.com/p/'
url='https://www.jianshu.com/search/do'
param= {'q': '', 'page': '1', 'type': 'note'}
errnum=0

def initpageElement(slug):
    li=[]
    html=requests.get(postfix+slug).text
    ele=etree.HTML(html)
    title=ele.xpath('/html/body/div[1]/div[1]/div[1]/h1')[0].text
    li.append(html)
    li.append(ele)
    # title=title.decode('utf-8','ignore').replace('/|\|:|?|"|>|<',' ')
    # title=title.decode('GB18030','ignore')
    try:
        title=re.sub('[/\\\\:*?"<>|]','', title)
    except Exception,e:
        print title
        li.append('a')
    else:
        li.append(title)
    return li


def PageHtmlDownload(slug,directory):
    li=initpageElement(slug)
    filename=directory+li[2]+'_2'+'.txt'
    if len(filename)<50:
        with open(filename,'w') as f:
            f.write(li[0].encode('utf-8'))


def PageDownload(slug,directory):
    li=initpageElement(slug)
    filename=directory+li[2]+'_1'+'.txt'
    if len(filename)<50:
        text = li[1].xpath('/html/body/div[1]/div[1]/div[1]/div[2]/div/p')
        with open(filename,'w') as f:
            f.write('from www.jianshu.com/p/'+slug+'\n')
            for i in text:
                if i is not None and i.text is not None:
                    f.write(i.text.encode('utf-8') + '\n')

def topicdownload(topic):
    directory1="d:/jianshu/"+topic+"/1/"
    directory2="d:/jianshu/"+topic+"/2/"
    if not os.path.exists(directory1):
        os.makedirs(directory1)
    if not os.path.exists(directory2):
        os.makedirs(directory2)
    param['q']=topic
    for i in range(1,101):
        param['page']=i
        try:
            entries=requests.post(url,data=param).json()['entries']
            for entry in entries:
                #slug是唯一标识文章的编号
                slug=entry['slug']
                PageDownload(slug,directory2)
                PageHtmlDownload(slug,directory1)
        except Exception as e:
            print 'error happen'




def topicGetter(topics):
    for topic in topics:
        topicdownload(topic)









if __name__=='__main__':
    topics=[u'大数据']
    topicGetter(topics)





