#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import re
import json
import sys
import os
import time

from datetime import datetime
from bs4 import BeautifulSoup

HEADERS = {
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", # noqa
     # "Accept-Encoding": "gzip, deflate",
    # "Accept-Language": "zh-CN,zh;q=0.9,zh-TW;q=0.8,en;q=0.7,ja;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    # "Cookie": "pgv_pvi=8494895104",
    # "Cookie": "",
    "Host": "www5.ncwu.edu.cn",
    # "Pragma": "no-cache",
    # "Referer": "http://www5.ncwu.edu.cn/channels/4.html",
    "Referer": "www5.ncwu.edu.cn",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",  # noqa
}


def get_data_from_pageurl_list(pageurl_list):
    result = {}

    for pageurl in pageurl_list:
        result.update(get_data_from_pageurl(pageurl))

    return result


def get_data_from_pageurl(pageurl):
    '''
    visit a page url, and return a dict which includes 12 notices's data.  
    '''
    print("resolve {}...\n".format(pageurl))

    if pageurl == 'http://www5.ncwu.edu.cn/channels/5.html':
        page_num = 1
    else:
        page_num = re.search(r'http://www5.ncwu.edu.cn/channels/5_(?P<page_num>\d+).html', pageurl).group('page_num')

    resp = requests.get(pageurl, headers=HEADERS)
    resp.encoding = 'utf-8'
    pattern = re.compile(
        # department
        r'<li>\s+【<a href="http://www5.ncwu.edu.cn/channels/\d*.html" class="dw">(?P<department>.+)'
        # href
        r'</a>】\s+<a href="http://www5.ncwu.edu.cn/contents/(?P<href>.+)\.html"'
        # title and create_time
        r' target="_blank"><span> (?P<title>.+) </span> </a><i>(?P<create_time>\d{4}-\d{2}-\d{2})</i></li>'
    )
    matches = re.finditer(pattern, resp.text)

    data = {}
    for match in matches:
        href = "http://www5.ncwu.edu.cn/contents/{}.html".format(match.group('href'))
        data[href] = {}
        
        data[href]['page_num'] = page_num
        data[href]['department'] = match.group('department')
        data[href]['title'] = match.group('title')
        data[href]['href'] = href
        data[href]['create_time'] = match.group('create_time')

    return data



def get_text(noticeurl):
    resp = requests.get(noticeurl, headers=HEADERS)
    soup = BeautifulSoup(resp.content, 'lxml')
    # get text
    # children includes tag and navigablestring
    xinxi_con_children = soup.find('div', class_='xinxi_con').children

    paragraphs = [n.text for n in xinxi_con_children if n.name == 'p']
    text = '\n'.join(paragraphs)

    return text


def create_pageurl_list(startpage_num, endpage_num):
    pageurl_list = []
    for i in range(startpage_num, endpage_num+1):
        if i == 1:
            pageurl_list.append('http://www5.ncwu.edu.cn/channels/5.html')

        else:
            pageurl_list.append(
                'http://www5.ncwu.edu.cn/channels/5_{}.html'.format(i))

    return pageurl_list


# def main():
#     root_dir = datetime.now().strftime('%Y%m%d_%H_%M_%S_ncwu_notice')
#     os.mkdir(root_dir)

#     startpage_num = 1
#     endpage_num = 10

#     pageurl_list = create_pageurl_list(startpage_num, endpage_num)

#     data = get_data_from_pageurl_list(pageurl_list)

#     count = 0
#     page = 1
#     for key, value in data.items():

#         if count % 12 == 0:
#             page_dir_path = os.path.join(root_dir, 'notice_5_' + str(page))
#             os.mkdir(page_dir_path)
#             page += 1
#         count += 1

#         file_name = '[{}][{}][{}]'.format(
#             value['department'], value['title'], value['create_time'])
#         file_name = file_name.replace('/', '')
#         file_name = file_name.replace('\\', '')

#         text_save_path = os.path.join(page_dir_path, file_name + '.txt')
#         text = get_text(key)

#         with open(text_save_path, 'w', encoding='utf-8') as f:
#             print("get {} ".format(key))
#             f.write(text)
#     print("---------------------------\n")
#     print("download completed. download dir path : {} \n".format(
#         os.path.join(os.getcwd(), root_dir)))


if __name__ == '__main__':
    # main()
    url = 'http://www5.ncwu.edu.cn/channels/5_2.html'
    pageurl_list = create_pageurl_list(1, 2)
    result = get_data_from_pageurl_list(pageurl_list)
    print(result)