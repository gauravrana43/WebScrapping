import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get('https://quotes.toscrape.com/')
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.prettify())

quote = soup.findAll('span', class_='text')
dict1 = {
    'quotes': [],
    'author': []
}
for item in quote:
    dict1['quotes'].append(item.text)

author = soup.findAll('div', class_='quote')
for item in author:
    dict1['author'].append(item.findAll('span')[1].find('small', class_='author').text)

df=pd.DataFrame(dict1)
df.to_csv('sc.csv',index=False)





