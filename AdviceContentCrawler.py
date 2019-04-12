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

def fetch_wenda_content(url):
    ''' not implemented yet'''
    pass

''' 根据URL来抓取内容 '''
def fetch_doctorteam_content(url):
    
    dict = {}
    dict["url"] = url
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
    req = urllib2.Request(url, headers=headers) 
    response = urllib2.urlopen(req, timeout=5)
    
    if response.getcode() !=200:
        print "wrong cqtch on \"" + url+"\""
    else:
        print "catching "+url
        html_cont = response.read()
        
        html_cont.decode("GBK").encode("UTF-8")
        soup = BeautifulSoup(html_cont,"html5lib")
        
        titleNode = soup.findAll("h2", class_="f-c-r-w-title")
        if not titleNode is None and len(titleNode)>0:
            dict["price"] = titleNode[0].get_text().strip()
            print "\tprice = "+ dict["price"]
            
        titles = soup.findAll("h4", class_ = "f-c-r-w-subtitle")
        print "\tlen of titles = "+str(len(titles))
        
        if not titles is None and len(titles)>0:
            for title in titles:
                value = title.find_next("p", class_ = "f-c-r-w-text")
                if not value is None:
                    t = title.get_text().strip()
                    v = value.get_text().strip()
                    print "\tTITLE "+t + " = VALUE "+v
                    dict[t] = v
            
    return dict

'''将每个咨询结果，写入文件中 '''
def write_dict_to_file(dict, target_file):
    file = open(target_file, "wb")
    for x in dict.keys():
        file.write(x+"=>"+dict[x]+"\n")
    file.close()
    print "CONTENT has been written into "+target_file
        
def fetch_allcontent(question_dir, target_dir, from_index, to_index):
    
    alread_done_set = set()

    have_done_log = question_dir+"/have_done.log"
    if not os.path.exists(have_done_log):
        have_done_log_file = open(have_done_log, "wb")
        have_done_log_file.write("")
        have_done_log_file.close()
    else:
        lines = open(have_done_log, "rb").read().split("\n")
        if not lines is None and len(lines)>0:
            for line in lines:
                if not line is None and len(line)>0:
                    alread_done_set.add(line.strip())
    
    files = os.listdir(question_dir)      
    files.sort()  
    for file in files:
        if file.endswith("_doctor.txt"):
            
            if file.strip() in alread_done_set: continue
            
            number_of_doctor = file.split("_")[1]
            number_of_doctor_value = int(number_of_doctor)
            
            if number_of_doctor_value<from_index or number_of_doctor_value >to_index: continue
            
            print "PROCESSING "+file
            f = open(question_dir+"/"+file, "rb")
            lines = f.read().split("\n")
            f.close()
            
            if not lines is None and len(lines)>0:
                count = 0
                for line in lines:
                    count = count + 1
                    url = line.strip()
                    if url.startswith("//"):
                        url = "https:"+url
                    print "URL = "+url
                    try:
                        dct = None
                        if url.find("doctorteam")>=0: 
                            dct = fetch_doctorteam_content(url)
                        if url.find("wenda")>=0:
                            dct = fetch_wenda_content(url)
                        if not dct is None and len(dct.keys())>0:
                            new_content_file = "content_"+ number_of_doctor+"_"+str(count)+".txt"
                            target_file = target_dir + "/"+new_content_file
                            write_dict_to_file(dct, target_file)
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
                        
            
            have_done_log_file = open(have_done_log, "a")
            have_done_log_file.write(file+"\n")
            have_done_log_file.close()

''' 执行抓取咨询内容的爬虫的执行入口， from_index, 和to_index是医生的顺序编号 '''
def execute():
    advice_list_dir = "/Users/retire2053/TEMP/advicelist"
    target_dir = "/Users/retire2053/TEMP/advicecontent"
    from_index = 1
    to_index = 6000
    fetch_allcontent(advice_list_dir, target_dir, from_index, to_index)
    
execute()
