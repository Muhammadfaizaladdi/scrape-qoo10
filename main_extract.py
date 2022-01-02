import pandas as pd
import extract
import time
import random
import requests

URL = "https://www.qoo10.my/gmkt.inc/Bestsellers/?banner_no=12021"

html_content = extract.extract_cont(URL)
parsed_content = extract.parse_cont(html_content, 'html.parser')
links = extract.get_list_link(parsed_content, 'a', 15, 'class', 'thmb')

# get data
list_of_content = []
for link in links:
    time.sleep(random.randint(10, 30))
    content = requests.get(link).text
    parsed_content = extract.parse_cont(content, 'html.parser')
    dict_content = {}
    dict_content['product_name'] = parsed_content.find('div', {'class' : 'goods-info'}).find('h2', {'class' : 'goods-detail__name'}).text
    if parsed_content.find('ul', {'class' : 'goods_path_lst'}):
        dict_content['category'] = parsed_content.find('ul', {'class' : 'goods_path_lst'}).find('span', {'itemprop' : 'name'}).text
        dict_content['sub_category'] = parsed_content.find('ul', {'class' : 'goods_path_lst'}).find('li', {'id' : 'depMenu4'}).find('span').text
    else:
        dict_content['category'] = None
        dict_content['sub_category'] = None
    if parsed_content.find('div', {'class' : 'goods-info'}).find('div', {'class' : 'prc'}):
        dict_content['price'] = parsed_content.find('div', {'class' : 'goods-info'}).find('div', {'class' : 'prc'}).find('strong').text
    else :
        dict_content['price'] = parsed_content.find('dl', {'class' : 'detailsArea lsprice'}).find('dd').find('strong').text
    if parsed_content.find('div', {'class' : 'grpbuy_area'}):
        dict_content['purchased'] = parsed_content.find('div', {'class' : 'grpbuy_area'}).find('div', {'class' : 'num'}).find('strong').text
    else:
        dict_content['purchased'] = None
    dict_content['del_rate'] = parsed_content.find('ul', {'class' : 'infoArea'}).find('div', {'class' : 'shpp_opt'}).find('em').text
    dict_content['shop_name'] = parsed_content.find('div', {'class' : 'goods-shopinfo'}).find('div', {'class' : 'goods-shopinfo__info'}).find('span', {'class' : 'name'}).text
    dict_content['location'] = parsed_content.find('div', {'class' : 'goods-shopinfo'}).find('div', {'class' : 'goods-shopinfo__info'}).find('span', {'class' : 'flag'}).find('dfn').get('title')
    dict_content['shop_rate'] = parsed_content.find('div', {'class' : 'goods-shopinfo'}).find('div', {'class' : 'goods-shopinfo__dtls'}).find('span', {'class' : 'mshop_rt'}).find('span').text
    if parsed_content.find('div', {'class' : 'goods-shopinfo'}).find('div', {'class' : 'goods-shopinfo__dtls'}).find('ul', {'class' : 'dtls'}).find('span'):
        dict_content['shop_items'] = parsed_content.find('div', {'class' : 'goods-shopinfo'}).find('div', {'class' : 'goods-shopinfo__dtls'}).find('ul', {'class' : 'dtls'}).find('span').text
    else:
        dict_content['shop_items'] = parsed_content.find('div', {'class' : 'goods-shopinfo'}).find('div', {'class' : 'goods-shopinfo__dtls'}).find('ul', {'class' : 'dtls'}).find('em').text
    if parsed_content.find('div', {'class' : 'goods-shopinfo'}).find('div', {'class' : 'goods-shopinfo__dtls'}).find('ul', {'class' : 'dtls'}).select_one("ul li:nth-of-type(2)"):
        dict_content['fellows'] = parsed_content.find('div', {'class' : 'goods-shopinfo'}).find('div', {'class' : 'goods-shopinfo__dtls'}).find('ul', {'class' : 'dtls'}).select_one("ul li:nth-of-type(2)").find('em').text
    else:
        dict_content['fellows'] = None
    
    if parsed_content.find('div', {'class' : 'goods-shopsatis'}):
        if parsed_content.find('div', {'class' : 'goods-shopsatis'}).find('div', {'class' : 'goods-shopsatis__num'}):
            dict_content['sold_for_1year'] = parsed_content.find('div', {'class' : 'goods-shopsatis'}).find('div', {'class' : 'goods-shopsatis__num'}).find('strong').text
        else : 
            dict_content['sold_for_1year'] = None
        if parsed_content.find('div', {'class' : 'goods-shopsatis'}).find('div', {'id' : 'ctl00_div_recommend_rate'}):
            dict_content['recommended'] = parsed_content.find('div', {'class' : 'goods-shopsatis'}).find('div', {'id' : 'ctl00_div_recommend_rate'}).find('strong').text
        else:
            dict_content['recommended'] = None
        if parsed_content.find('div', {'class' : 'goods-shopsatis'}).find('div', {'id' : 'ctl00_div_satis_percent'}):
            dict_content['cust_satisfied'] = parsed_content.find('div', {'class' : 'goods-shopsatis'}).find('div', {'id' : 'ctl00_div_satis_percent'}).find('strong').text
        else:
            dict_content['cust_satisfied'] = None
        if parsed_content.find('div', {'class' : 'goods-shopsatis__cust'}).find('g', {'class' : 'stroke'}).find('g'):
            dict_content['product_rate'] = parsed_content.find('div', {'class' : 'goods-shopsatis__cust'}).find('g', {'class' : 'stroke'}).find('g').find('text').text
        else:
            dict_content['product_rate'] = None
        if parsed_content.find('div', {'class' : 'goods-shopsatis__cust'}).find('g', {'class' : 'stroke'}).select_one("g g:nth-of-type(2)"):
            dict_content['price_rate'] = parsed_content.find('div', {'class' : 'goods-shopsatis__cust'}).find('g', {'class' : 'stroke'}).select_one("g g:nth-of-type(2)").find('text').text
        else:
            dict_content['price_rate'] = None
        if parsed_content.find('div', {'class' : 'goods-shopsatis__cust'}).find('g', {'class' : 'stroke'}).select_one("g g:nth-of-type(3)"):
            dict_content['delivery_rate'] = parsed_content.find('div', {'class' : 'goods-shopsatis__cust'}).find('g', {'class' : 'stroke'}).select_one("g g:nth-of-type(3)").find('text').text
        else:
            dict_content['delivery_rate'] = None
        if parsed_content.find('div', {'class' : 'goods-shopsatis__cust'}).find('g', {'class' : 'stroke'}).select_one("g g:nth-of-type(4)"):
            dict_content['service_rate'] = parsed_content.find('div', {'class' : 'goods-shopsatis__cust'}).find('g', {'class' : 'stroke'}).select_one("g g:nth-of-type(4)").find('text').text 
        else:
            dict_content['service_rate'] = None
    else:
        dict_content['sold_for_1year'] = None
        dict_content['recommended'] = None
        dict_content['cust_satisfied'] = None
        dict_content['product_rate'] = None
        dict_content['price_rate'] = None
        dict_content['delivery_rate'] = None
        dict_content['service_rate'] = None
    list_of_content.append(dict_content)


data = pd.DataFrame(list_of_content)
data.to_csv('output/data.csv')