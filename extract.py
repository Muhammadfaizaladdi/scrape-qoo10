import requests
from bs4 import BeautifulSoup

# extract content 
def extract_cont(url):
    html_content = requests.get(url).text
    return html_content

# parsing content
def parse_cont(html_content, parser_type):
    parsed_html_cont = BeautifulSoup(html_content, parser_type)
    return parsed_html_cont

# get all content
def get_all_content(parsed_cont, tag, attr_type=None, attr_val=None):
    get_html_content = parsed_cont.find_all(tag, {attr_type:attr_val})
    return get_html_content

# Get single content
def get_single_content(parsed_cont, tag, attr_type=None, attr_val=None):
    get_html_content = parsed_cont.find(tag, {attr_type:attr_val})
    return get_html_content

# Get link product
def get_list_link(content, tag, max_link, attr_type=None, attr_val=None):
    link_with_text = []
    cnt = 1
    for a in content.find_all(tag, {attr_type:attr_val}):
        link_with_text.append(a['href'])

        if cnt == max_link:
            break
        cnt += 1
    return link_with_text