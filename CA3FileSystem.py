#CA3 File System

import os
import requests
from requests import get, post
import json
from dateutil import parser
import datetime
import bs4
import re

'''

# This is initial experiments on FILE SYSTEM management

'''


# pwd = os.system("pwd")
# print(pwd)

# f = open('practice.txt','w+')
# f.write('test')
# f.close()

# print(os.getcwd())

# print(os.listdir())



# import shutil

# shutil.move('practice.txt','/workspace/General/wk11')

# os.listdir()

# shutil.move('/workspace/General/wk11/practice.txt',os.getcwd())

# os.listdir()



# import send2trash

# print(os.listdir())

# send2trash.send2trash('practice.txt')

# print(os.listdir())



# print(os.getcwd())

# print(os.listdir())

# for folder , sub_folders , files in os.walk("wk1"):

#     print("Currently looking at folder: "+ folder)
#     print('\n')
#     print("THE SUBFOLDERS ARE: ")
#     for sub_fold in sub_folders:
#         print("\t Subfolder: "+sub_fold )

#     print('\n')

#     print("THE FILES ARE: ")
#     for f in files:
#         print("\t File: "+f)
#     print('\n')

# # #

# weekNumber = 1
# wkx = str(weekNumber)

# for w in os.walk("wk"+wkx):
#     weekWalk = w

# listwk = weekWalk[2]
# print (listwk)

# print(weekWalk)

# linkSlides = "https://mikhail-cct.github.io/ca3-test/wk"+wkx
# linkPDF = "https://mikhail-cct.github.io/ca3-test/wk"+wkx+"/wk"+wkx+".pdf"

# print(linkSlides)
# print(linkPDF)
# https://mikhail-cct.github.io/ca3-test/wk1
# https://mikhail-cct.github.io/ca3-test/wk1.pdf

def file_links(wkNumber):
    wkx = str(wkNumber)
    linkSlides = "https://mikhail-cct.github.io/ca3-test/wk"+wkx
    linkPDF = "https://mikhail-cct.github.io/ca3-test/wk"+wkx+"/wk"+wkx+".pdf"
    for w in os.walk("wk"+wkx):
        weekWalk = w
        file_listwk = weekWalk[2]
        html_push = []
        if "wk"+wkx+".pdf" in file_listwk:
            html_push.append(linkPDF)
        if "slides.md" in file_listwk:
            html_push.append(linkSlides)
        return html_push

# print (file_links(3))

wkx = 1



# index_title = open('wk1/index.html',"r").read()
index_title = open(f"wk{wkx}/index.html","r").read()
title_soup = bs4.BeautifulSoup(index_title,"lxml")
print(title_soup.select('title')[0].getText())

# f = open(f"{name}.csv", 'wb') 
