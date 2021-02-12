import requests
from pyquery import PyQuery as pq
import pymongo
import re
import time

client = pymongo.MongoClient(host='localhost',port=27017)
db = client['data']
collection = db['mv_data']

    
#抓取网页
def scrape_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 Edg/88.0.705.63'
    }
    rep = requests.get(url,headers=headers)
    if rep.status_code == 200:
        print('抓取成功')
        return rep.text
    else:
        print(f'抓取失败,网站为{url},状态码为{rep.status_code}')
# html=scrape_page(url_a)
# print(html)

#抓取详情页的网址
def scrape_url(html):
    b_url=[]
    doc = pq(html)
    links = doc('#content li .info a')
    for link in links.items():
        href = link.attr('href')
        b_url.append(href)
    return b_url

# 抓取数据(详情页)
# 抓取电影名称、导演、类型、语言、上映时间
def get_data(html):
    doc = pq(html)
    a = doc('#info').text()
    mv_name = doc('#content h1>span:first-child').text()
    mv_director = re.search('^导演: (.*)',a).group(1)
    mv_type = re.search('类型: (.*?)\n',a,re.S).group(1)
    mv_language =re.search('语言: (.*?)\n',a,re.S).group(1)
    mv_time = re.search('上映日期: (.*?)\n',a,re.S).group(1)
    mv_score = doc('#interest_sectl .rating_num').text()
    return {
        'mv_name':mv_name,
        'mv_director':mv_director,
        'mv_type':mv_type,
        'mv_language':mv_language,
        'mv_time':mv_time,
        'mv_score':mv_score
    }

#储存数据
def save_data(note):
    collection.insert_one(note)


# 网址生成器

#第一页、第二页
for i in range(0,26,25):
    # print(i)
    a_url = f'https://movie.douban.com/top250?start={i}&filter='
    html = scrape_page(a_url)
    for url in scrape_url(html):
        time.sleep(5)
        h = scrape_page(url)
        save_data(get_data(h))
        print(f'保存成功')
print('完成')

#第三页、第四页
# for i in range(50,76,25):
#     # print(i)
#     a_url = f'https://movie.douban.com/top250?start={i}&filter='
#     html = scrape_page(a_url)
#     for url in scrape_url(html):
#         time.sleep(5)
#         h = scrape_page(url)
#         save_data(get_data(h))
#         print(f'保存成功')
# print('完成')

#第五页、第六页
# for i in range(100,126,25):
#     # print(i)
#     a_url = f'https://movie.douban.com/top250?start={i}&filter='
#     html = scrape_page(a_url)
#     for url in scrape_url(html):
#         time.sleep(5)
#         h = scrape_page(url)
#         save_data(get_data(h))
#         print(f'保存成功')
# print('完成')

#第七页、第八页
# for i in range(150,176,25):
#     # print(i)
#     a_url = f'https://movie.douban.com/top250?start={i}&filter='
#     html = scrape_page(a_url)
#     for url in scrape_url(html):
#         time.sleep(5)
#         h = scrape_page(url)
#         save_data(get_data(h))
#         print(f'保存成功')
# print('完成')

#第九页、第十页
# for i in range(200,226,25):
#     # print(i)
#     a_url = f'https://movie.douban.com/top250?start={i}&filter='
#     html = scrape_page(a_url)
#     for url in scrape_url(html):
#         time.sleep(5)
#         h = scrape_page(url)
#         save_data(get_data(h))
#         print(f'保存成功')
# print('完成')
