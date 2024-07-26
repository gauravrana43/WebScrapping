import pandas as pd
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error

url = 'https://quotes.toscrape.com/'


def send_to_sql(data):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='########',
            database='quotes'
        )
        print("SQL server Connected")
        cursor = connection.cursor()
        tableName = 'quotesAuthor'
        insertionQuery = f"""
        Insert Into {tableName}
        Values
        (%s,%s)
        """
        values = [(item['quotes'], item['author']) for item in data]
        # print(values)
        cursor.executemany(insertionQuery, values)
        connection.commit()
    except Error as e:
        print(f"Error is {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Sql server disconnected")


def qa(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    containers = soup.findAll('div', class_='quote')
    for item in containers:
        quotes = item.find('span', class_='text').text
        author = item.findAll('span')[1].find('small').text
        dict1 = {
            'quotes': quotes,
            'author': author
        }
        data.append(dict1)

    try:
        next_page = 'https://quotes.toscrape.com' + soup.find('li', class_='next').find('a').get('href')
    except:
        next_page = None
    if next_page:
        qa(next_page)


if __name__ == '__main__':
    data = []
    qa(url)
    df = pd.DataFrame(data)
    df.to_csv('QuotesAndAuthor.csv')
    send_to_sql(data)
