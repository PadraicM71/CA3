# CA3 Main
import requests
from requests import get, post
import json
from dateutil import parser
import datetime
import bs4
import re
import os


# This is a year 'switch' to assign to script for each repository its used in.
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


# linkId complete list of unique recording google identifiers - starting at index 1.
# Create a list containing all individual class recording unique 33 characters google ID.
linkConstruct = []
for link in re.finditer(r'"(\S{33})",\S"1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"',gdrive):
    linkConstruct.append(link.group(1))
# Above Regex returns duplicate list - remove last half to have just 1 complete list.
linkId = linkConstruct[:len(linkConstruct)//2]
linkId.insert(0, " ") # Insert blank at index 0 - we will use this later to represent case where no recording available yet
# print(linkId) # debug


# https://drive.google.com/file/d/14pVDe0l1SYcpQxqsfW32modTbxhMEIcJ/view?usp=sharing # testing


# titleId complete list of unique recording class title identifiers - starting at index 1.
# Create a list containing all individual class recording titles.
titleConstruct = []
for title in re.finditer(r',"(20\d\d-\d\d-\d\d.*.mp4)","',gdrive):
    titleConstruct.append(title.group(1))
# Above Regex returns duplicate list - remove last half to have just 1 complete list.
titleId = titleConstruct[:len(titleConstruct)//2]
titleId.insert(0, "Class recording not available yet - Please try later. ")
number_of_recordings = len(titleId) ########################################### used later to calculate iso week - take note!
# Insert message at index 0 - we will use this later to represent case where no recording available yet
# print(titleId) # debug


#----------------------------------------------------------------------------------------------------------------------------------
# Takes date of recording from title str scraped off GoogleDrive page
# It then converts it to a date object
# Can now extract ISO week number
# recDate = (titleId[1][:10])
# recDateObj = datetime.datetime.strptime(recDate, '%Y-%m-%d')
# print(recDateObj.date())
# print(recDateObj.strftime("%V"))
#-------------------------------------------------------------------------------------------------------------------------------------


def classRecording(number):
    x = '<a href=\"https://drive.google.com/file/d/' + linkId[number] + '/view?usp=sharing\"' + '>' + titleId[number] + '</a>'
    return x # print('<a href=\"https://drive.google.com/file/d/' + linkId[weekNumber] + '/view?usp=sharing\"' + '>' + titleId[weekNumber] + '</a>')



def read_summary(wk): # Reads summary content of given week
    summary_content = json.dumps(sec.getsections[wk]['summary'], indent=4, sort_keys=True)
    return summary_content



# Function to write to Moodle summary
# wk is Moodle page section number
def write_summary(wk, link): # update sections wk1 section 1 etc
    summary = link
    data[0]['summary'] = summary
    data[0]['section'] = wk
    sec_write = LocalUpdateSections(courseid, data)
    return
# link = '<a href="https://drive.google.com/file/d/1elgdm2482AMcARz_NUVTjg8KBPmoLTxj/view?usp=sharing">2020-10-06 [17:45-19:44] – Prog: OO Approaches.mp4</a>'



#-----------------------------------------------------------------------------------------------------------
def iso_week_number_moodle(week):
    date = parser.parse(list(sec.getsections)[week]['name'].split('-')[0])
    date = date.replace(year=semesterStartYear) # force year on it as its using current year date
    date = date.strftime("%V")
    return date
# print(iso_week_number_moodle(5))

def iso_week_number_recordings(title_from_recording_list):
    # Takes date of recording from title str scraped off GoogleDrive page
    # It then converts it to a date object
    # Can now extract ISO week number
    recDate = (titleId[title_from_recording_list][:10]) # take date information from string titleId
    recDateObj = datetime.datetime.strptime(recDate, '%Y-%m-%d') # make date object
    return (recDateObj.strftime("%V")) # return iso week number
# print(iso_week_number_recordings(3))


# Merge any list to a string - needed to push string to Moodle
def merged_list_to_string(any_list):
    merged_list = ''
    for element in any_list:
        merged_list += str(element)
    return merged_list



# ok experimenting looks good here - keep error free by linking to number of recordings - defined above titleId
def match_week_to_recordings(week_number):
    n=1
    rec = []
    while n < number_of_recordings: # index 0 not used implies dont need <= (only require <)
        if iso_week_number_recordings(n) == iso_week_number_moodle(week_number):
            rec.append(classRecording(n)+"<br>")
        n+=1
    return rec

link = '<a href="https://drive.google.com/file/d/1elgdm2482AMcARz_NUVTjg8KBPmoLTxj/view?usp=sharing">2020-10-06 [17:45-19:44] – Prog: OO Approaches.mp4</a>'
# Construct file links - Initial experiements!
def file_links(wkNumber):
    wkx = str(wkNumber)
    linkSlides = '<a href=' + "https://mikhail-cct.github.io/ca3-test/wk" + wkx + '>Slides Week ' + wkx + '</a>'
    linkPDF = '<a href=' + "https://mikhail-cct.github.io/ca3-test/wk" + wkx + "/wk" + wkx + ".pdf" + ">Week" + wkx + '.pdf</a>'
    for w in os.walk("wk"+wkx):
        weekWalk = w
        file_listwk = weekWalk[2]
        html_push = []
        if "wk"+wkx+".pdf" in file_listwk:
            html_push.append(linkPDF+"<br>")
        if "slides.md" in file_listwk:
            html_push.append(linkSlides+"<br>")
        print(linkSlides)
        print(linkPDF)
        return html_push



# print(match_week_to_recordings(8))


# Experimenting 
# # Assemble the payload for push to summary in a list for_push
# for_push = match_week_to_recordings(1)
# write_summary(5, match_week_to_recordings(1))


#Assemble payload for push
# Final object for push has to be continious string with appropriate HTML tags
# It will be assembled here
# payload = [] # this will be used for push to moodle
# payload.append("test<br>")
# # print(payload)
# payload.append(merged_list_to_string(match_week_to_recordings(8))) # merge_list to string for all further additions
# print(payload)
# payload_for_push = (merged_list_to_string(payload))


# Testing complete push of recordings - It works!! Excellent!! Keep it simple!
n=1
while n<9: 
    write_summary(n,merged_list_to_string(match_week_to_recordings(n)+file_links(n)))
    n+=1


# print (file_links(3))
# print(merged_list_to_string(file_links(3)))


# print(read_summary(2))
