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
number_of_recordings = len(titleId) ############################## used later to calculate/manipulate iso week - take note!

# The above creates 2 lists where the index of each match the recording unique identifier with the correct recording title.
# Recordings identifiers capture complete.



'''

Script Functions

'''

# Constructs a complete class recording link (as a string) with html tags ready for push.
# Uses linkId and titleId from above Regex.
# Parameter passed is recording number as it appears on Regex generated lists (linkId, titleId)
def classRecording(number):
    construct_link_rec = '<a href=\"https://drive.google.com/file/d/' + linkId[number] + '/view?usp=sharing\"' + '>' + titleId[number] + '</a>'
    return construct_link_rec


# Reads summary content of a given week.
# Parameter passed is week number.
def read_summary(wk):
    summary_content = json.dumps(sec.getsections[wk]['summary'], indent=4, sort_keys=True)
    return summary_content


# Function to write to Moodle summary for specific week.
# Parameters passed:
# wk is Moodle page week/summary number.
# link will be the final string of concatenated list items containing appropriate html tags for push.
def write_summary(wk, link):
    summary = link
    data[0]['summary'] = summary
    data[0]['section'] = wk
    sec_write = LocalUpdateSections(courseid, data)
    return


# Function to convert Moodle week name (which is a date, day and month name) to an ISO week number.
# Parameter is week number.
def iso_week_number_moodle(week):
    date = parser.parse(list(sec.getsections)[week]['name'].split('-')[0])
    # Above reads name from Moodle week number and converts it to a date object.
    date = date.replace(year=semesterStartYear)
    # Above forces year on it as it was using current year date script is run which could be different.
    # It is essential to have correct year of semester in order to generate correct ISO week numbers.
    date = date.strftime("%V") # Now convert it to an ISO week number.
    return date


# Function to take date of recording from title str scraped off GoogleDrive page.
# It then converts it to a date object.
# Can now extract ISO week number.
# Parameter passed is index from recording titleId.
def iso_week_number_recordings(title_from_recording_list):
    recDate = (titleId[title_from_recording_list][:10]) # take date information from string titleId
    recDateObj = datetime.datetime.strptime(recDate, '%Y-%m-%d') # make it a date object
    return (recDateObj.strftime("%V")) # return iso week number


# Function to merge any list to a string.
# It is needed to push a string to Moodle that already has appropriate html tags.
# Parameter passed is the list.
def merged_list_to_string(any_list):
    merged_list = ''
    for element in any_list:
        merged_list += str(element)
    return merged_list

# Function to create required hyperlinks for Recordings to push to Moodle week summary.
# Creates a string to represent the recordings for a specific ISO week number.
# The created string contains appropriate html tags ready for push to Moodle.
# For the specific week number passed, all the recordings are iterated over to find matching ISO weeks numbers.
# If there is 1 or more recondings for that week they will be appended to the string.
# There is no limit to the number of recordings that can be added for a specific week.
# Equally important, if there is no recording for that week nothing will be returned and no error will be generated.
# Kept error free by linking to number of recordings - defined above.
# Parameter passed is Moodle week number.
def match_week_to_recordings(week_number):
    n=1
    rec = []
    while n < number_of_recordings: # index 0 not used implies dont need <= (only require <)
        if iso_week_number_recordings(n) == iso_week_number_moodle(week_number):
            rec.append(classRecording(n)+"<br>") # appends complete class recording string with html tag.
        n+=1
    return rec


# Function to create required hyperlinks for Slides and PDF docs to push to Moodle week summary.
# Parameter passed is week number.
def file_links(wkNumber):
    wkx = str(wkNumber) # convert week number to string to construst hyperlink.
    # first get title from index.html
    index_title = open(f"wk{wkx}/index.html","r").read() # Open index.html for week number.
    title_soup = bs4.BeautifulSoup(index_title,"lxml") # Using bs4 to parse file.
    title_notes = title_soup.select('title')[0].getText() # Get title only without tags.
    # Create links
    # Next construct our hyperlinks as a continious string with correct html tags for push to Moodle.
    linkSlides = '<a href=' + "https://mikhail-cct.github.io/ca3-test/wk" + wkx + '>Week ' + wkx + " Slides: " + title_notes + '</a>'
    linkPDF = '<a href=' + "https://mikhail-cct.github.io/ca3-test/wk" + wkx + "/wk" + wkx + ".pdf" + ">Week " + wkx + ' PDF file: ' + title_notes + '</a>'
    for w in os.walk("wk"+wkx):
        weekWalk = w # This is a tuple of wk_number folder information
        file_listwk = weekWalk[2] # Here get the third element of that tuple which is a list of that directory contents.
        html_push = [] # Create empty list for push to Moodle.
        if "wk"+wkx+".pdf" in file_listwk: # If the PDF file is present append it with appropriate html tag.
            html_push.append(linkPDF+"<br>")
        if "slides.md" in file_listwk: # If the slides.md file is present append it with appropriate html tag.
            html_push.append(linkSlides+"<br>")
        # Therefore using above method, if a file is missing it won't return an error.
        print(linkSlides)
        print(linkPDF)
        return html_push # returns string with appropriate html tags ready for push to Moodle.




# ---------------DO NOT DELETE-------------------------------------------------
# Testing complete push of recordings - It works!! Excellent!! Keep it simple!
directory = os.listdir()
number_of_folders_wkx = len([folder for folder in directory if "wk" in folder])
week_num_to_update = 1
while week_num_to_update < number_of_folders_wkx: 
    write_summary(week_num_to_update,merged_list_to_string(match_week_to_recordings(week_num_to_update)+file_links(week_num_to_update)))
    week_num_to_update += 1
# -----------------------------------------------------------------------------



#ENDS