import json

import pandas as pd
import requests
from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import Error
def send_data_to_sql(data):
    try:
        conn=mysql.connector.connect(
            host='localhost',
            user='root',
            password='########',
            database='books_data',
        )
        if conn.is_connected():
            print("Sql server started")
        cursor=conn.cursor()
        data_insert=[(item['url'],item['name'],item['price'],item['rating'],item['image_url'],item['description'],item['category'])for item in data]
        insert_query="""
        Insert into book_details
        Values(%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.executemany(insert_query,data_insert)
        conn.commit()
    except Error as e:
        print(f"Error is {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("SQL server closed")

def extract_book_detail(book_url,data):
    print("entered")
    response=requests.get(book_url)
    soup=BeautifulSoup(response.content,'html.parser')
    product=soup.findAll('div',class_='page_inner')[1]
    product_dict={
        'url':book_url,
        'name':product.find('article',class_='product_page').find('div',class_='col-sm-6 product_main').find('h1').text,
        'price':product.find('article',class_='product_page').find('div',class_='col-sm-6 product_main').find('p',class_='price_color').text,
        'rating':len(product.find('article',class_='product_page').find('div',class_='col-sm-6 product_main').findAll('i',class_='icon-star')),
        'image_url':product.find('article',class_='product_page').find('img').get('src'),
        'description': product.find('article',class_='product_page').findAll('p')[3].text,
        'category':product.find('ul',class_='breadcrumb').findAll('li')[2].text
        }
    table_list=product.findAll('tr')

    table_dict={}
    for item in table_list:
        table_dict[item.find('th').text]=item.find('td').text
    print(product_dict)
    data.append(product_dict)
    file=open('table_details.json','w')
    json_result=json.dump(table_dict,file)



def extract_each_book_url(url,data):
    print('entered')
    response=requests.get(url)
    soup= BeautifulSoup(response.content,'html.parser')
    list_items=soup.findAll('li', class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for items in list_items:
        book_url=url+ items.find('h3').find('a').get('href')
        extract_book_detail(book_url,data)

# def every_page(url,data):
#     response=requests.get(url)
#     soup=BeautifulSoup(response.content,'html.parser')
#     extract_each_book_url(url, data)
#     try:
#         next_page_url=url+soup.find('li',class_='next').find('a').get('href')
#     except:
#         next_page_url=None
#     if next_page_url:
#         every_page(next_page_url,data)



if __name__ == '__main__':
    data=[]
    url="https://books.toscrape.com/"
    # every_page(url,data)
    extract_each_book_url(url,data)
    send_data_to_sql(data)
