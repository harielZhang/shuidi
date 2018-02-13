# -*- coding: utf8 -*-
import BeautifulSoup
import requests
import json
import time
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

headers = {
    "Host":"www.shuidixy.com",
    "Connection":"keep-alive",
    "Cache-Control":"max-age=0",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch",
    "Accept-Language":"zh-CN,zh;q=0.8"
    }


def Requests(url):
    
    headers["User-Agent"] = random.choice(user_agent_list).strip()
    ip = random.choice(ip_list).strip()
    proxies = {
              "http": "http://" + ip,
              "https": "http://" + ip,
            }

    response = requests.get(url = url, headers = headers, proxies=proxies, timeout=30)

    # print url
    # print ip
    print response
    # print response.status_code
    # print response.text
    # print "\n"

    return response


def get_base_info(company_id):
    url = 'http://www.shuidixy.com'+company_id
    re = Requests(url)
    re.encoding = 'utf-8'
    #整个页面
    allhtml = re.text
    return allhtml


def download_html(com_name, startnum, endnum):
    with open('./data/' + com_name + '.txt', 'r') as file:
        company_list = file.readlines()
    # print(company_list)
    starttime = time.time()

    for i, company in enumerate(company_list[startnum:endnum]):
        company_name = str(company).split('_')[-1].replace('.txt', '').strip()
        print ">>>>>>>>>>" + str(i) + "_" + company_name + "<<<<<<<<<<"
        html_save_path = (r"./html/" + company_name + ".html").decode('utf8')
        try:
            # time.sleep(random.uniform(0, 1))
            url = 'http://www.shuidixy.com/search?key=' + company_name + '&searchType=all&entry=0&npage=0'
            re = Requests(url)
            re.encoding = 'utf-8'
            soup = BeautifulSoup(re.text, "lxml")
            print(soup)
            content = soup.find('div', attrs={'class':'or_search_list'}).find('div', attrs={'class':'or_search_row_content'})
            company_id = content.find('a').get('href').strip()
            print company_id
            allhtml = get_base_info(company_id)

            with open(html_save_path, 'w') as file:
                file.write(allhtml)
            print 'right'
        except:
            with open(r"./log_download.txt", 'a') as file:
                file.write(company_name + '\n')
            print 'wrong'
        if i % 100 == 0:
            print i, (time.time()-starttime) / 60



# if __name__ == '__main__':
    