# CA3 Main
import requests
from requests import get, post
import json
from dateutil import parser
import datetime
import bs4
import re

semesterStartYear = 2020

'''

# Location to build the main SCRIPT
# Moodle analysis to take place here
# Later will merge with CA3FileSystem.py and CA3Recordings.py

'''
# Module variables to connect to moodle api:
# Insert token and URL for your site here.
# Mind that the endpoint can start with "/moodle" depending on your installation.
KEY = "8cc87cf406775101c2df87b07b3a170d"
URL = "https://034f8a1dcb5c.eu.ngrok.io"
ENDPOINT = "/webservice/rest/server.php"


def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.
    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict == None:
        out_dict = {}
    if not type(in_args) in (list, dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args) == list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args) == dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict


def call(fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.
    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update(
        {"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    # print(parameters)
    response = post(URL+ENDPOINT, data=parameters).json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response

################################################
# Rest-Api classes
################################################


class LocalGetSections(object):
    """Get settings of sections. Requires courseid. Optional you can specify sections via number or id."""

    def __init__(self, cid, secnums=[], secids=[]):
        self.getsections = call('local_wsmanagesections_get_sections',
                                courseid=cid, sectionnumbers=secnums, sectionids=secids)


class LocalUpdateSections(object):
    """Updates sectionnames. Requires: courseid and an array with sectionnumbers and sectionnames"""

    def __init__(self, cid, sectionsdata):
        self.updatesections = call(
            'local_wsmanagesections_update_sections', courseid=cid, sections=sectionsdata)

################################################
# Example
################################################


courseid = "4"  # Exchange with valid id.
# Get all sections of the course.
sec = LocalGetSections(courseid)

#----------------------------------------------------------------------------
# Output readable JSON, but print only summary
# print(json.dumps(sec.getsections[0]['summary'], indent=4, sort_keys=True))

# # Split the section name by dash and convert the date into the timestamp, it takes the current year, so think of a way for making sure it has the correct year!
# month = parser.parse(list(sec.getsections)[1]['name'].split('-')[0])
# # Show the resulting timestamp
# print(month)
# # Extract the week number from the start of the calendar year
# print(month.strftime("%V"))

#  Assemble the payload
data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]

# # Assemble the correct summary
# summary = '<a href="https://mikhail-cct.github.io/ca3-test/wk1/">Week 1: IntroductionTest1</a><br>' # note different quotes

# # Assign the correct summary
# data[0]['summary'] = summary

# # Set the correct section number
# data[0]['section'] = 4

# Write the data back to Moodle
# sec_write = LocalUpdateSections(courseid, data)
#---------------------------------------------------------------------------------------
# Writing Information: (updatesections)


# # Function to write to Moodle summary
# # wk is Moodle page section number
# def writeLink(wk, link): # update sections wk1 section 1 etc
#     summary = link
#     data[0]['summary'] = summary
#     data[0]['section'] = wk
#     sec_write = LocalUpdateSections(courseid, data)
#     return
# link = '<a href="https://drive.google.com/file/d/1elgdm2482AMcARz_NUVTjg8KBPmoLTxj/view?usp=sharing">2020-10-06 [17:45-19:44] – Prog: OO Approaches.mp4</a>'
# writeLink(2, link)


#---------------------------------------------------------------------------------------

# Read Information
sec = LocalGetSections(courseid)

# print(json.dumps(sec.getsections[0]['summary'], indent=4, sort_keys=True))
# print(json.dumps(sec.getsections[0]['name'], indent=4, sort_keys=True))
# print(json.dumps(sec.getsections[0]['sectionnum'], indent=4, sort_keys=True))
# print("------------------------------------------------------")
# print(json.dumps(sec.getsections[1]['summary'], indent=4, sort_keys=True))
# # we want to write the summary!
# # get back a dictionary from the API - grab key called summary
# print(json.dumps(sec.getsections[1]['sectionnum'], indent=4, sort_keys=True))
# print(json.dumps(sec.getsections[1]['name'], indent=4, sort_keys=True))
# print("------------------------------------------------------")
# print(json.dumps(sec.getsections[2]['summary'], indent=4, sort_keys=True))
# print(json.dumps(sec.getsections[2]['sectionnum'], indent=4, sort_keys=True))
# print(json.dumps(sec.getsections[2]['name'], indent=4, sort_keys=True))
# print("------------------------------------------------------")
# print(json.dumps(sec.getsections[15]['summary'], indent=4, sort_keys=True))
# print("Dates Below -------------------------------------------------------------")
# Reading Information: (getsections)
# can now identify way to loop (for) through sections any maybe build dictionary
# of all of the slides that are present in any of the sections if you like.
# get section - grab title and start doing things with it.
# So thats reading our information sorted!
#--------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------
#Recordings
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
print(titleId) # debug




# Dates

# Split the section name by dash and convert the date into the timestamp, it takes the current year, so think of a way for making sure it has the correct year!
date1 = parser.parse(list(sec.getsections)[1]['name'].split('-')[0])

# print(date1.strftime("%x"))
# This is date from Moodle
# date1 = parser.parse(list(sec.getsections)[1]['name'].split('-')[0])
# date1 = date1.replace(year=semesterStartYear) # force year on it as its using current year date
# print(date1)
# print(date1.strftime("%V")) # gets ISO week number
# print(type(date1))
# dateOne = str(date1)
# dateTwo = (dateOne[:10])
# print(dateTwo)
# print(type(dateTwo))
# # print(dateOne)
# dateOneObj = datetime.datetime.strptime(dateTwo, '%Y-%m-%d')
# # # dateOneObj = date1.strftime("2020-%m-%d")
# # print (dateOneObj)
# print(dateOneObj.strftime("%V"))



# Takes date of recording from title str scraped off GoogleDrive page
# It then converts it to a date object
# Can now extract ISO week number
recDate = (titleId[1][:10])
recDateObj = datetime.datetime.strptime(recDate, '%Y-%m-%d')
print(recDateObj.date())
print(recDateObj.strftime("%V"))



# idtest = "14pVDe0l1SYcpQxqsfW32modTbxhMEIcJ"
# testId = 'https://drive.google.com/file/d/' + idtest + '/view?usp=sharing'
# print(testId)

# print(titleId[8] + "  LINK: " + 'https://drive.google.com/file/d/' + linkId[8] + '/view?usp=sharing')


def classRecording(number):
    x = '<a href=\"https://drive.google.com/file/d/' + linkId[number] + '/view?usp=sharing\"' + '>' + titleId[number] + '</a>'
    return x # print('<a href=\"https://drive.google.com/file/d/' + linkId[weekNumber] + '/view?usp=sharing\"' + '>' + titleId[weekNumber] + '</a>')

classRecording(2)

# <a href="https://drive.google.com/file/d/1vyPoSlUc5hcXajllDyaqMKvlJOiYxbNH/view?usp=sharing">2020-09-29 [18:46-19:44] – Prog: OO Approaches.mp4</a><br>"test"

#-------------------------------------------
# Writing Information: (updatesections)

# Function to write to Moodle summary
# wk is Moodle page section number
def write_summary(wk, link): # update sections wk1 section 1 etc
    summary = link
    data[0]['summary'] = summary
    data[0]['section'] = wk
    sec_write = LocalUpdateSections(courseid, data)
    return
# link = '<a href="https://drive.google.com/file/d/1elgdm2482AMcARz_NUVTjg8KBPmoLTxj/view?usp=sharing">2020-10-06 [17:45-19:44] – Prog: OO Approaches.mp4</a>'


# Experimenting 
# Assemble the payload for push to summary in a list for_push
for_push = (classRecording(5)+'<br>'+"newline2"+'<br>'+classRecording(6))

write_summary(5, for_push)

def iso_week_number_moodle(week):
    date = parser.parse(list(sec.getsections)[week]['name'].split('-')[0])
    date = date.replace(year=semesterStartYear) # force year on it as its using current year date
    date = date.strftime("%V")
    return date

print(iso_week_number_moodle(5))

def iso_week_number_recordings(week):
    # Takes date of recording from title str scraped off GoogleDrive page
    # It then converts it to a date object
    # Can now extract ISO week number
    recDate = (titleId[week][:10])
    recDateObj = datetime.datetime.strptime(recDate, '%Y-%m-%d')
    return (recDateObj.strftime("%V"))

print(iso_week_number_recordings(3))

end_week = 8
# def gather_recordings(week):
#     for end_week in 



# Takes date of recording from title str scraped off GoogleDrive page
# It then converts it to a date object
# Can now extract ISO week number
# recDate = (titleId[1][:10])
# recDateObj = datetime.datetime.strptime(recDate, '%Y-%m-%d')
# print(recDateObj.date())
# print(recDateObj.strftime("%V"))

# date1 = parser.parse(list(sec.getsections)[1]['name'].split('-')[0])
# date1 = date1.replace(year=termStartYear) # force year on it as its using current year date
# print(date1)
# print(date1.strftime("%V")) # gets ISO week number


