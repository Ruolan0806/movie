import requests
from lxml import etree
from fake_useragent import UserAgent
base= 'https://www.ygdy8.net/'
ua= UserAgent()
headers = {'User-Agent': ua.random}


def get_detail_urls(url):
    proxy = '123.58.10.36:8080'  # 本地代理
    # proxy='username:password@123.58.10.36:8080'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }

    # url = 'https://www.ygdy8.net/html/gndy/dyzz/list_23_1.html'
    response= requests.get(url, headers= headers)
    text = response.content.decode('gbk','ignore')
    html=etree.HTML(text)
    details_url = html.xpath("//table[@class = 'tbspan']//a//@href")
    details_url=map(lambda url: base+url,details_url)
    # for i in details_url:
    #     print (i)
    return details_url


def parse_detail_page(url):
    movie={}
    response=requests.get(url, headers=headers)
    text = response.content.decode('gbk', 'ignore')
    html = etree.HTML(text)
    title=html.xpath('//div[@class= "title_all"]//font[@color="#07519a"]//text()')[0]
    movie['title']=title
    zoom=html.xpath('//div[@id="Zoom"]')[0]
    cover= zoom.xpath('.//img//@src')
    movie['cover'] = cover[0]
    info=zoom.xpath('.//text()')
    for i in info:
        if i.startswith('◎年　　代'):
            year = i.replace('◎年　　代','').strip()
            movie['year'] = year
        elif i.startswith('◎产　　地'):
            area = i.replace('◎产　　地', '').strip()
            movie['country'] = area
        elif i.startswith('◎类　　别'):
            category = i.replace('◎类　　别', '').strip()
            movie['category'] = category
        elif i.startswith('◎IMDb评分'):
            rating = i.replace('◎IMDb评分', '').strip()
            movie['rating'] = rating
        elif i.startswith('◎导　　演'):
            director = i.replace('◎导　　演', '').strip()
            movie['director'] = director
    download=html.xpath('//td[@bgcolor = "#fdfddf"]/a/@href')
    if len(download)>0:
        download_url=download[0]
    else:
        download_url=''
    movie['download']= download_url
    # print(movie)
    return movie


def spider():
    movies=[]
    base_url='https://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html'
    for x in range(1,8):
        url=base_url.format(x)
        detail_urls=get_detail_urls(url)
        for i in detail_urls:
            movie = parse_detail_page(i)
            movies.append(movie)
            print(movie)


if __name__ == '__main__':
    spider()
