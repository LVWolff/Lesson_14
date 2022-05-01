
import csv
from bs4 import BeautifulSoup
import requests
import re

def normal_text(string):
    return re.sub(r'\W', r' ', string).strip()


URL = 'https://telik.pro/reviews/xiaomi'

page = requests.get(URL)

# print(page.status_code)

soup = BeautifulSoup(page.text, 'html.parser')

reviews = soup.find_all('div', class_ = 'comment-comment-text')

# print(len(reviews))

# csv.Dictwriter

data_dict = []
fieldnames = ['dignity','negative', 'comment']


for review in reviews:
    temp_txt = review.getText()
    start_dignity = temp_txt.find('Достоинства')
    start_negative = temp_txt.find('Недостатки')
    start_comnt = temp_txt.find('Комментарий')

    dignity = normal_text(temp_txt[(start_dignity + 11):start_negative-1].strip())
    negative = normal_text(temp_txt[(start_negative + 10):start_comnt-1].strip())
    comment = normal_text(temp_txt[(start_comnt + 11):].strip())

    # из строки надо убрать спецсимволы и лишние переносы.

    dict_line = {'dignity': dignity, 'negative': negative, 'comment': comment}
    data_dict.append(dict_line)

print(data_dict)

with open('reviews.csv', 'w') as f:
     writer = csv.DictWriter(f,delimiter = ';',fieldnames=fieldnames)
     writer.writeheader()
     for i in range(len(data_dict)):
        writer.writerow(data_dict[i])



