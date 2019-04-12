#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import sys
import os
import time
import re
import ssl
import socket

reload(sys) 
sys.setdefaultencoding('UTF-8')
SLEEP_INTERVAL = 5

SEPARATOR = "\n"

''' 五种要抓取的病种，以及每个病种的有多少页 '''
''' 因为初始设定页面数很容易，所以并不需要代码直接来抓取'''
diseases = [["feiyan", 304], ["xiaochuan", 224],[ "manzhufei", 87], [ "feiqizhong", 67],[ "zhiqiguanyan", 203]]

''' 抓取一个病种的所有医生，将结果保存在目标文件夹下 '''
def fetch_doctorlist_for_one_disease(disease, fromcount, tocount, target_dir):
    ''' p是用来分页的变量 '''
    for p in range(fromcount, tocount+1, 1):
        url = ""
        if p == 1 :
            url = "https://www.haodf.com/jibing/"+disease+"/daifu_all_all_all_all_all.htm"
        else:
            url = "https://www.haodf.com/jibing/"+disease+"/daifu_all_all_all_all_all_"+str(p)+".htm"
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
        
        try:
            req = urllib2.Request(url, headers=headers) 
            response = urllib2.urlopen(req)
            result = []
            if response.getcode() !=200:
                print "wrong cqtch on \"" + url+"\""
            else:
                print "catching "+url
                html_cont = response.read()
                html_cont.decode("GBK").encode("UTF-8")
                soup = BeautifulSoup(html_cont,"html5lib")
                doctor_nodes = soup.findAll('div', class_ = "doc_rela_link")
                for node in doctor_nodes:
                    anchor = node.find("a")
                    if not anchor is None:
                        result.append(anchor["href"])                
        except UnicodeDecodeError:
            print "DECODE ERROR,Skip content"
        except urllib2.URLError:
            print "URL ERROR, Skip content and sleep "+str(SLEEP_INTERVAL)+" seconds"
            time.sleep(SLEEP_INTERVAL)
        except urllib2.HTTPError:
            print "HTTP ERROR, Skip content and sleep "+str(SLEEP_INTERVAL)+" seconds"
            time.sleep(SLEEP_INTERVAL)
        except ssl.SSLError:
            print "SSL ERROR, Skip content and sleep "+str(SLEEP_INTERVAL)+" seconds"
            time.sleep(SLEEP_INTERVAL)
        except socket.error:
            print "SOCKET ERROR, Skip content and sleep "+str(SLEEP_INTERVAL)+" seconds"
            time.sleep(SLEEP_INTERVAL)    
        
        ''' 将每个疾病的每个医生列表，保存在一个单独的文件中。在该文件中，每行是一个医生 '''
        file = open(target_dir+"/"+disease+"_page_"+str(p), "wb")
        for x in result:
            file.write(x+SEPARATOR)
        file.close()
        print "保存第"+str(p)+"页医生列表，疾病=\"" + disease+"\"" 

def fetch_all_doctors(target_dir):   
    for p in range(len(diseases)):
        disease = diseases[p]
        fetch_doctorlist_for_one_disease(disease[0], 1, disease[1], target_dir)

''' 不同病种下有重复的医生，用set将其过滤，最终保存一个不含重复的医生列表 '''
def remove_duplicate_doctor(target_dir, target_path):
    filelist = os.listdir(target_dir)
    theset = set()
    for file in filelist:
        print "processing "+file
        file = open(target_dir + "/"+file, "rb")
        content = file.read()
        file.close()
        
        lines = content.split(SEPARATOR)
        for line in lines:
            if len(line.strip())>0:
                theset.add(line)
    
    print "After removing duplicate doctors, there are "+str(len(theset)) +" doctors left"
    
    final_file_path = target_dir+"/"+target_path
    file = open(final_file_path, "wb")
    for item in theset:
        file.write(item+SEPARATOR)
    file.close()
    print "FINAL doctor list has been saved to "+final_file_path+"!"
    
''' 抓取医生列表的爬虫的执行入口'''    
def execute():
    target_dir = "/Users/retire2053/TEMP/doctorlist"
    fetch_all_doctors(target_dir)
    remove_duplicate_doctor(target_dir, "final_doctor_list.txt")

execute()
    