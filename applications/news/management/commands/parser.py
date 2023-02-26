import requests
from bs4 import BeautifulSoup as BS
import csv
import datetime
from datetime import timedelta
import celery


url = 'https://www.igromania.ru/news/'
host = 'https://www.igromania.ru'

def news():
    
    response = requests.get(url)
    soup = BS(response.text, 'lxml')
    items = soup.find_all('div', class_='aubl_item')
    news = []
    count = 1
    for item in items:
        now = datetime.datetime.now()
        formatted_date = now.strftime("%d.%m.%Y")
        if not str(formatted_date) in str(item.find('div', class_="aubli_date").text):
            break
        news.append(item.text.strip()+'\n')
        news.append(host+item.find('a', class_="aubli_img").get('href')+'\n\n')
        print(formatted_date)
        
        count += 1
        if count == 100:
            break
    with open('data.txt', 'w') as file:
        for i in news:
            file.write(str(i))

def news2():
    response2 = requests.get(url)
    soup2 = BS(response2.text, 'lxml')
    items2 = soup2.find_all('div', class_='aubl_item')
    oldnews = []
    count = 0
    for item in items2:
        today = datetime.datetime.today()
        yesterday = today - timedelta(days=1)
        if not str(yesterday.strftime('%d.%m.%Y')) in str(item.find('div', class_="aubli_date").text):
            continue
        oldnews.append(item.text.strip()+'\n')
        oldnews.append(host+item.find('a', class_="aubli_img").get('href')+'\n\n')
    
        
        count += 1
        if count == 100:
            break
    with open('minus.txt', 'w') as file:
        for i in oldnews:
            file.write(str(i))



