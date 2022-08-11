import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from IPython.display import HTML

key = "PS5" #여기에 서칭 하고자 하는 키워드 입력, 그냥 최신 게시물 보고 싶을 땐 공백 한칸
pages = 10 #사이트 별로 표시할 최대 페이지 수

products = [] #List to store name of the product
link = []
website = []
time = []

def ruliweb(keyword):

    url = "\fhttps://bbs.ruliweb.com/market/board/1020?search_type=subject&search_key={}".format(keyword)
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    body = soup.find(attrs={"class": "board_main theme_default theme_white"})
    i = 0
    for a in body.findAll('tr', attrs={'class': 'table_body blocktarget'}):
        if i < pages:
            deal = a.find('a', attrs={'class': 'deco'}, href=True)
            products.append(deal.text)
            link.append(deal.get("href"))
            website.append("Ruliweb")
            time.append(a.find('td', attrs={'class': 'time'}).text.strip())
            i += 1



def yepan(keyword):

    url = "\fhttp://yepan.net/bbs/board.php?bo_table=local_info&sca=&sfl=wr_subject&stx={}&sop=and&x=0&y=0".format(keyword)
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    body = soup.select_one('#fboardlist > table > tbody')
    for a in body.select('td.mw_basic_list_subject > div.mw_basic_list_subject_desc'):
        print(a)
        products.append(a.text)
        link.append(a.select('a')[-1]['href'])
        website.append("Yepan")
    for b in body.findAll('td', attrs={'class': 'mw_basic_list_datetime'}):
        timestamp = b.text
        time.append(timestamp)


def clien(keyword):

    url = "\fhttps://www.clien.net/service/search?q={}&sort=recency&boardCd=jirum&isBoard=true".format(keyword)
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    body = soup.find(attrs={"class": "contents_jirum"})
    i = 0
    for a in body.findAll('span', attrs={'class': 'list_subject'}):
        if i < pages:
            deal = a.find('a', attrs={'class': 'subject_fixed'}, href=True)
            products.append(deal.get("title"))
            link.append("https://www.clien.net" + deal.get("href"))
            website.append("Clien")
            i += 1
    i = 0
    for b in body.findAll('span', attrs={'class': 'timestamp'}):
        if i < pages:
            time.append(b.text[0:10].replace('-', '.'))
            i += 1

def coolenjoy(keyword):

    url = "\fhttps://coolenjoy.net/bbs/jirum?bo_table=jirum&sca=&sop=and&sfl=wr_subject&stx={}".format(keyword)
    html = requests.get(url).text

    soup = BeautifulSoup(html, "html5lib")
    body = soup.find('tbody')
    i = 0
    for a in body.findAll('td', attrs={'class': 'td_subject'}):
        if i < pages:
            deal = a.text.strip()
            products.append(deal)
            link.append(a.find('a').get("href"))
            website.append("Coolenjoy")
            i += 1
    i = 0
    for b in body.findAll('td', attrs={'class': 'td_date'}):
        if i < pages:
            time.append('20' + b.text[0:10].replace('-', '.'))
            i += 1

ruliweb(key)
clien(key)
coolenjoy(key)

df = pd.DataFrame({'Date':time, 'Website':website, 'Title':products, 'Link':link})
e = datetime.datetime.now()
today = e.strftime("%Y.%m.%d")
for idx, i in df.iterrows():
    if len(i['Date']) < 10:
        df.at[idx, 'Date'] = today
sorteddf = df.sort_values(by=['Date'], ascending=False)

def make_clickable(url, name):
    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url,name)
    
sorteddf['Title'] = sorteddf.apply(lambda x: make_clickable(x['Link'], x['Title']), axis=1)
viewdf = sorteddf[['Date', 'Website', 'Title']].copy()
HTML(viewdf.to_html(render_links=True, escape=False))

#sorteddf.to_csv('\f{}_{}.csv'.format(key, today), index=False, encoding='utf-8')
