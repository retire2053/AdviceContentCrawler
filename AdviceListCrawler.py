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

''' 抓取某一个医生的所有咨询列表 '''    
def fetch_advicelist_for_one_doctor(no,total, url,target_dir):
    print "Start processing No.["+str(no)+"/"+str(total) +"] "+url
    
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'} 
    req = urllib2.Request(url, headers=headers) 
    response = urllib2.urlopen(req)
    result = []
    
    if response.getcode() !=200:
        print "\twrong cqtch on \"" + url+"\""
    else:
        print "\tcatching "+url
        html_cont = response.read()
        
        html_cont.decode("GBK").encode("UTF-8")
        soup = BeautifulSoup(html_cont,"html5lib")
                
        link_nodes = soup.findAll('a', class_ = "rela_dis")
        for node in link_nodes:
            result.append(node["href"])
        
        bottom_nodes = soup.findAll("a", class_ = "page_turn_a")
        count = 1
        if not bottom_nodes is None and len(bottom_nodes)>0:
            
            tet = bottom_nodes[-1].get_text()
            items = tet.split(" ")
            count = int(items[1])
        print "\ttotal page count is "+str(count)
        
        if count>=2:
            for p in range(2, count+1, 1):
                try:
                    newurl = url + "?p_type=all&p="+str(p)
                    req = urllib2.Request(newurl, headers=headers) 
                    response = urllib2.urlopen(req)
                    if response.getcode() !=200:
                        print "\twrong cqtch on \"" + newurl+"\""
                    else:
                        print "\tcatching "+newurl
                        html_cont = response.read()
                        html_cont.decode("GBK").encode("UTF-8")
                        soup = BeautifulSoup(html_cont,"html5lib")
                                
                        link_nodes = soup.findAll('a', class_ = "rela_dis")
                        for node in link_nodes:
                            result.append(node["href"])
                except urllib2.URLError:
                    print "URL Error page.["+str(p)+"/"+str(count)+"], sleep 20 seconds"
                    time.sleep(SLEEP_INTERVAL)
                except urllib2.HTTPError:
                    print "HTTP Error. page.["+str(p)+"/"+str(count)+"], sleep 20 seconds"
                    time.sleep(SLEEP_INTERVAL)
                except UnicodeDecodeError:
                    print "DECODE ERROR, page.["+str(p)+"/"+str(count)+"]"
                except ssl.SSLError:
                    print "SSL ERROR, page.["+str(p)+"/"+str(count)+"] sleep "+str(SLEEP_INTERVAL)+" seconds"
                    time.sleep(SLEEP_INTERVAL)
                except socket.error:
                    print "SOCKET ERROR,page.["+str(p)+"/"+str(count)+"] sleep "+str(SLEEP_INTERVAL)+" seconds"
                    time.sleep(SLEEP_INTERVAL)    
    file = open(target_dir+"/no_"+str(no)+"_doctor.txt", "wb")
    for item in result:
        file.write(item+"\n")
    file.close()
        
    print "FINISH processing No.["+str(no)+"/"+str(total) +"] "+url +", item="+str(len(result))

''' 抓取全部医生的全部咨询列表 '''
def fetch_advicelist_for_all_doctor(doctor_list_filepath, target_dir):
    file = open(doctor_list_filepath, "rb")
    content = file.read()
    file.close()
    
    lines = content.split("\n")
    total = len(lines)
    print "total "+str(total)+" are found in repository"
    error_path = target_dir+"/error_doctors.txt"
    file = open(error_path, "wb")
    file.write("")
    file.close()
    
    for p in range(1, len(lines)+1, 1):
        print "" 
        line = lines[p-1]
        print "find URL = "+line
        if not line.startswith("//"): continue
        
        if line.endswith(".htm") : 
            print "ESCAPE No.["+str(p)+"/"+str(total)+"]"
            continue
        
        url = "https:"+line.strip()+"zixun/list.htm"
        try:
            fetch_advicelist_for_one_doctor(p,total, url, target_dir)
            time.sleep(2)
        except urllib2.URLError:
            print "URL Error No.["+str(p)+"/"+str(total)+"], sleep 20 seconds"
            time.sleep(SLEEP_INTERVAL)
            append_error(error_path, line, p, total)
        except urllib2.HTTPError:
            print "HTTP Error. No.["+str(p)+"/"+str(total)+"], sleep 20 seconds"
            time.sleep(SLEEP_INTERVAL)
            append_error(error_path, line, p, total)
        except UnicodeDecodeError:
            print "DECODE ERROR, No.["+str(p)+"/"+str(total)+"]"
            append_error(error_path, line, p, total)
        except ssl.SSLError:
            print "SSL ERROR, No.["+str(p)+"/"+str(total)+"] sleep "+str(SLEEP_INTERVAL)+" seconds"
            time.sleep(SLEEP_INTERVAL)
            append_error(error_path, line, p, total)
        except socket.error:
            print "SOCKET ERROR,No.["+str(p)+"/"+str(total)+"] sleep "+str(SLEEP_INTERVAL)+" seconds"
            time.sleep(SLEEP_INTERVAL)    
            append_error(error_path, line, p, total)

''' 将错误文件，放在错误日志中 '''   
def append_error(error_path, line, p, total):
    file = open(error_path, "a")
    file.write(line+"\n")
    file.close()
    print "APPEND No.["+str(p)+"/"+str(total)+"] to ERROR FILE"    

''' 抓取咨询列表的爬虫的执行入口 '''
''' 本爬虫，依赖于DoctorListCrawler '''
def execute():
    doctor_list_filepath = "/Users/retire2053/TEMP/doctorlist/final_doctor_list.txt"
    target_dir = "/Users/retire2053/TEMP/advicelist"
    fetch_advicelist_for_all_doctor(doctor_list_filepath, target_dir)

execute()
    