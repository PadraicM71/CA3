import requests
import bs4
import re


'''

# This is initial experiments to capture RECORDING links and titles

'''



res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX")


# print(type(res))

# print(res.text)

#--------

soup = bs4.BeautifulSoup(res.text,"lxml")

# print(soup)

print(soup.select('title'))
# # these 4 lines good
# title_tag = soup.select('title')
# print(title_tag[0])
# print(type(title_tag[0]))
# print(title_tag[0].getText())

# print(soup.select('.pmHCK'))

# for item in soup.select("true"):
#     print(item.text)


gdrive = res.text

# vLink = re.search(r'.*\n.*\.mp4',gdrive)
vLink = re.search(r'.*\n.*\.mp4',gdrive)
print(vLink)

# vTitle = re.findall(r'\,\"([^\"]*\.mp4)\"',gdrive)
# print(vTitle)

'''
EXPERIEMENT:

# vTitle2 = re.findall(r'data-id="(\S{33})"',gdrive) # this works
# print(vTitle2)

# vTitle3 = re.search(r'"(\S{33})",\S"1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"',gdrive)
# print (vTitle3.group(1))

# vTitle3 = re.search(r'"(\S{33})",\S"1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"',gdrive)
# print (vTitle3.group(1))

# [["1vyPoSlUc5hcXajllDyaqMKvlJOiYxbNH",["1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"]
# ,"2020-09-29 [18:46-19:44] – Prog: OO Approaches.mp4","video/mp4"

'''

#This is working now - complete list of unique recording links
for match in re.finditer(r'"(\S{33})",\S"1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"',gdrive):
    print(match.group(1))

