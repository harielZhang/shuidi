# -*- coding: utf8 -*-
from download_html import *
from extract_data import *
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def cmd_list_com_name():
	command ="dir html\\*.html /b>html\\company_name.txt"
	os.system(command)

if __name__ == '__main__':
	#download_html 传入公司名字， 爬虫起始位，爬虫结束位
	
	download_html('zjcom_name', 0, 11)
	cmd_list_com_name()
	# extract_data()