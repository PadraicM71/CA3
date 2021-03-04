# Not used anymore



import requests
import bs4
import re


'''

# This is initial experiments to capture RECORDING links and titles

'''



res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX")

soup = bs4.BeautifulSoup(res.text,"lxml")

gdrive = res.text


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

# ,"2020-09-29 [18:46-19:44] – Prog: OO Approaches.mp4","video/mp4"

'''

# This is working now - complete list of unique recording google identifiers.
# Create a list containing all individual class recording unique 33 characters google ID.
linkConstruct = []
for link in re.finditer(r'"(\S{33})",\S"1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"',gdrive):
    linkConstruct.append(link.group(1))
# Above Regex returns duplicate list - remove last half to have just 1 complete list.
linkId = linkConstruct[:len(linkConstruct)//2]
linkId.insert(0, " ") # Insert blank at index 0 - we will use this later to represent case where no recording available yet
# print(linkId) # debug


# https://drive.google.com/file/d/14pVDe0l1SYcpQxqsfW32modTbxhMEIcJ/view?usp=sharing # testing


#This is working now - complete list of unique recording class title identifiers
# Create a list containing all individual class recording titles.
titleConstruct = []
for title in re.finditer(r',"(20\d\d-\d\d-\d\d.*.mp4)","',gdrive):
    titleConstruct.append(title.group(1))
# Above Regex returns duplicate list - remove last half to have just 1 complete list.
titleId = titleConstruct[:len(titleConstruct)//2]
titleId.insert(0, "Class recording not available yet - Please try later. ")
# Insert message at index 0 - we will use this later to represent case where no recording available yet
# print(titleId) # debug



# idtest = "14pVDe0l1SYcpQxqsfW32modTbxhMEIcJ"
# testId = 'https://drive.google.com/file/d/' + idtest + '/view?usp=sharing'
# print(testId)

# print(titleId[8] + "  LINK: " + 'https://drive.google.com/file/d/' + linkId[8] + '/view?usp=sharing')


def classRecording(weekNumber):
    return print('<a href=\"https://drive.google.com/file/d/' + linkId[weekNumber] + '/view?usp=sharing\"' + '>' + titleId[weekNumber] + '</a>')

classRecording(2)

# <a href="https://drive.google.com/file/d/1vyPoSlUc5hcXajllDyaqMKvlJOiYxbNH/view?usp=sharing">2020-09-29 [18:46-19:44] – Prog: OO Approaches.mp4</a><br>"test"

'''

Ok - recording is complete and ready to merge with CA3Main - Can request a week and return a complete html construct for push to Moodle. Good going!

'''

