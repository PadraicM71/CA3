# CA3 script.py
import requests
from requests import get, post
import json
from dateutil import parser
import datetime
import bs4
import re
import os


# This is a year 'switch' to assign to script for each repository its used in.
# Set the semester start year after script file is inserted in repository.
# This is required for using ISO week numbers later.
# Once this is set the script needs no further changes for insertion to any year or
# any semester repository irrespective of semester number.
semesterStartYear = 2020 # script year switch


'''

Moodle Plug In

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


courseid = "4"  # Exchange with valid id.
# Get all sections of the course.
sec = LocalGetSections(courseid)
#  Assemble the payload.
data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]
sec = LocalGetSections(courseid)



'''

Recordings - Scraping video links and URL construction

'''
# Scrape appropriate Google Drive page containing video links using BeautifulSoap.
res = requests.get("https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX")
soup = bs4.BeautifulSoup(res.text,"lxml")
gdrive = res.text


# Recording - linkId - complete list of unique recording google identifiers - starting at index 1.
# Create a list containing all individual class recording unique 33 characters google ID.
# Using Regex and its group capture feature to extract exact link so no further processing needed.
linkConstruct = [] # create empty list
for link in re.finditer(r'"(\S{33})",\S"1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"',gdrive):
    linkConstruct.append(link.group(1))
# Above Regex returns duplicate list - remove last half to have just 1 complete list.
linkId = linkConstruct[:len(linkConstruct)//2]
linkId.insert(0, " ") # Insert blank at index 0 - we will use this later to represent case where no recording available yet.


# Recording - titleId - complete list of unique recording class title identifiers - starting at index 1.
# Create a list containing all individual class recording titles.
# Using Regex and its group capture feature to extract exact title so no further processing needed.
titleConstruct = []
for title in re.finditer(r',"(20\d\d-\d\d-\d\d.*.mp4)","',gdrive):
    titleConstruct.append(title.group(1))
# Above Regex returns duplicate list - remove last half to have just 1 complete list.
titleId = titleConstruct[:len(titleConstruct)//2]
titleId.insert(0, "Class recording not available yet - Please try later. ")
# Insert message at index 0 - can be used at a later stage to represent a case where no recording available yet.

# Calculate number of recordings for iteration later.
number_of_recordings = len(titleId) ############################## used later to calculate iso week - take note!




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


# Function to write to Moodle summary for specific week.
# wk is Moodle page week/summary number.
def write_summary(wk, link): # update sections wk1 summary 1 etc.
    summary = link
    data[0]['summary'] = summary
    data[0]['section'] = wk
    sec_write = LocalUpdateSections(courseid, data)
    return


def iso_week_number_moodle(week):
    date = parser.parse(list(sec.getsections)[week]['name'].split('-')[0])
    date = date.replace(year=semesterStartYear) # force year on it as its using current year date
    date = date.strftime("%V")
    return date


def iso_week_number_recordings(title_from_recording_list):
    # Takes date of recording from title str scraped off GoogleDrive page
    # It then converts it to a date object
    # Can now extract ISO week number
    recDate = (titleId[title_from_recording_list][:10]) # take date information from string titleId
    recDateObj = datetime.datetime.strptime(recDate, '%Y-%m-%d') # make date object
    return (recDateObj.strftime("%V")) # return iso week number


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
    # Grab title from html
    index_title = open(f"wk{wkx}/index.html","r").read()
    title_soup = bs4.BeautifulSoup(index_title,"lxml")
    title_notes = title_soup.select('title')[0].getText()
    # Create links
    linkSlides = '<a href=' + "https://mikhail-cct.github.io/ca3-test/wk" + wkx + '>Week ' + wkx + " Slides: " + title_notes + '</a>'
    linkPDF = '<a href=' + "https://mikhail-cct.github.io/ca3-test/wk" + wkx + "/wk" + wkx + ".pdf" + ">Week " + wkx + ' PDF file: ' + title_notes + '</a>'
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


# ---------------DO NOT DELETE-------------------------------------------------
# Testing complete push of recordings - It works!! Excellent!! Keep it simple!
directory = os.listdir()
number_of_folders_wkx = len([folder for folder in directory if "wk" in folder])
week_num_to_update = 1
while week_num_to_update < number_of_folders_wkx: 
    write_summary(week_num_to_update,merged_list_to_string(match_week_to_recordings(week_num_to_update)+file_links(week_num_to_update)))
    week_num_to_update += 1
# -----------------------------------------------------------------------------


