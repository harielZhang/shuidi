# -*- coding: utf8 -*-
import BeautifulSoup
import json
import time
import random

import sys
reload(sys)
sys.setdefaultencoding('utf-8')



def analysis(company_name):
    dic_base = {}
    dic_people = {}
    lis_people = []
    dic_gdxx = {}
    lis_gdxx = []
    dic_bgxx = {}
    lis_bgxx = []
    dic_dwtz = {}
    lis_dwtz = []
    html = open(r'./html/'+company_name+'.html', 'r')
    soup = BeautifulSoup(html, "lxml")
    # print soup
    #基本信息
    titles = soup.findAll('td', attrs={'class':'sh01'})
    values = soup.findAll('td', attrs={'class':'sh02'})
    for title, value in zip(titles, values):
        dic_base[title.get_text().strip()[:-1]] = value.get_text().replace('\t', '').replace('\r', '').replace('\n', '').replace(' ', '')
    str_json1 = str(json.dumps(dic_base))
    base_info = str_json1.decode('raw_unicode_escape')

    #高管信息
    names = soup.findAll('span', attrs={'class':'base_list_n1'})
    jobs = soup.findAll('span', attrs={'class':'base_list_n2'})
    for title, value in zip(names, jobs):
        temp_dic_people = {}
        temp_dic_people['name'] = title.get_text().strip()
        temp_dic_people['job'] = value.get_text().replace('\t', '').replace('\r', '').replace('\n', '').replace(' ', '')
        lis_people.append(temp_dic_people)
    dic_people['people'] = lis_people
    str_json2 = str(json.dumps(dic_people))
    people_info = str_json2.decode('raw_unicode_escape')

    #股东信息
    table = soup.findAll('tr', attrs={'class':'partnerContentCls'})
    for tr in table:
        gdmcs = tr.find('td', attrs={'class':'sh03'}).find('a')
        rjcjes = tr.findAll('td', attrs={'class':'sh04'})[0]
        sjczes = tr.findAll('td', attrs={'class':'sh04'})[1]
        cgbls = tr.findAll('td', attrs={'class':'sh04'})[2]
        for gdmc, rjcje, sjcze, cgbl in zip(gdmcs, rjcjes, sjczes, cgbls):
            temp_gdxx = {}
            temp_gdxx['gdmc'] = gdmc.strip()
            temp_gdxx['rjcje'] = rjcje.strip()
            temp_gdxx['sjcze'] = sjcze.strip()
            temp_gdxx['cgbl'] = cgbl.strip()
            lis_gdxx.append(temp_gdxx)
    dic_gdxx['gdxx'] = lis_gdxx
    str_json3 = str(json.dumps(dic_gdxx))
    gdxx_info = str_json3.decode('raw_unicode_escape')

    #真实名称
    real_company_name = soup.find('span', attrs={'class':'sd_mes_name'}).get_text().strip()

    #变更信息
    bgjls = soup.findAll('div', attrs={'class':'panel_jl_border'})
    for bgjl in bgjls:
        temp_bgxx = {}
        temp_bgxx['bgxm'] = bgjl.findAll('span')[0].get_text().strip()
        temp_bgxx['bgq'] = bgjl.findAll('span')[1].get_text().strip()
        temp_bgxx['bgdate'] = bgjl.findAll('span')[2].get_text().strip()
        temp_bgxx['bgh'] = bgjl.findAll('span')[3].get_text().strip()
        lis_bgxx.append(temp_bgxx)
    dic_bgxx['bgtotal'] = soup.find('div', attrs={'id':'changeTotal'}).find('small').get_text().strip()
    dic_bgxx['bgxx'] = lis_bgxx
    str_json4 = str(json.dumps(dic_bgxx))
    bgxx_info = str_json4.decode('raw_unicode_escape')

    #对外投资
    dwtzs = soup.findAll('div', attrs={'class':'investment'})
    for dwtz in dwtzs:
        temp_dwtz = {}
        temp_dwtz['company'] = dwtz.find('a').get_text().strip()
        lis_dwtz.append(temp_dwtz)
    dic_dwtz['dwtztotal'] = soup.find('li', attrs={'id':'outInvestTab'}).find('span').get_text().strip()
    dic_dwtz['dwtz'] = lis_dwtz
    str_json5 = str(json.dumps(dic_dwtz))
    dwtz_info = str_json5.decode('raw_unicode_escape')

    return real_company_name, base_info, people_info, gdxx_info, bgxx_info, dwtz_info


def extract_data():
    with open(r'./html/company_name.txt', 'r') as file:
        company_list = file.readlines()
    all_com = len(company_list)

    for index, company in enumerate(company_list):
        company_name = company.strip().replace('.html', '')
        real_company_name, base_info, people_info, gdxx_info, bgxx_info, dwtz_info = analysis(company_name)
        info = real_company_name+'\n'+base_info+'\n'+people_info+'\n'+gdxx_info+'\n'+bgxx_info+'\n'+dwtz_info
        
        with open(r"./txt/"+company_name+".txt", 'w') as file:
            file.write(info + '\n')
        print str(index+1)+'/'+str(all_com)
        break


# if __name__ == '__main__':