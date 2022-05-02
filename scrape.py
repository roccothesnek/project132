import requests
from bs4 import BeautifulSoup
import pprint

SESSION = requests.Session()

def moodleLogin(username, password):
    ''' Simply logs in the session to moodle, takes 2 strings for username and password, this must be called before scraping assignments '''
    
    
    # forget cookies
    SESSION.cookies.clear()
    
    # payload for login POST request
    loginData = {
        'username': username,
        'password': password,
        '_eventId': 'submit',
        'geolocation': ''
    }       
    
    # go to login page
    url = "https://cas.latech.edu/cas/login?service=https%3A%2F%2Fmoodle.latech.edu%2Flogin%2Findex.php"
    r = SESSION.get(url)
    
    # check if already logged in
    soup = BeautifulSoup(r.content, 'html5lib')
    if soup.find('form', id = 'fm1') != None:
        # use bs to find hidden title "execution" value and attach to payload
        soup = BeautifulSoup(r.content, 'html5lib')
        loginData['execution'] = soup.find('input', attrs={'name': 'execution'})['value']
        # send post request to log in
        r = SESSION.post(url, data = loginData)
        soup = BeautifulSoup(r.content, 'html5lib')
        # return 1 if the login was successful, -1 if unsuccessful
        if soup.find('form', id = 'fm1') != None:
            return -1
        else:
            return 1
    # if SESSION cant get webpage, return -1
    else:
        return -1
    
def getMoodleAssignments():
    ''' Once session is logged in, this will pull every event (unfiltered) and return a list of dictionaries for each event '''
    assignmentDictList = []
    # go to calendar page
    url = "https://moodle.latech.edu/calendar/view.php?view=upcoming"
    r = SESSION.get(url)
    
    # uses bs to find all events, dates, and classes
    soup = BeautifulSoup(r.content, 'html5lib')
    # get all events
    for event in soup.find_all('div', class_ = "event mt-3"):
        # get event name and date
        eventName = event.h3.text
        eventDate = event.find('div', class_ = "col-11")
        # look for class row in page
        for eventClassRow in event.find_all('div', class_ = "row mt-1"):
            # get potential class row
            potEventClass = eventClassRow.find('div', class_ = "col-11")
            # determine if this row contains the class name
            if potEventClass.a != None:
                eventClass = potEventClass.text
        assignmentDictList.append({
            'Event': eventName,
            'Date': eventDate.text,
            'Class': eventClass
        })
    if assignmentDictList != []:
        return assignmentDictList
    else:
        return None

def webworkLogin(username, password, className):
    ''' Logs the session in to webwork, takes 3 strings, the username, password, and the EXACT name of the webwork class, must be called before scraping off webwork '''
    
    # payload for POST login request
    loginData = {
        'user': username,
        'passwd': password
    }
    
    # send post request
    url = "https://webwork.latech.edu/webwork2/" + className + "/"
    r = SESSION.post(url, data = loginData)
    
def getWebworkAssignments(className):
    ''' Once session is logged in, this will pull every assignment (unfiltered) and return a list of dictionaries for each event '''
    assignmentDictList = []
    # get the webpage
    url = "https://webwork.latech.edu/webwork2/" + className + "/"
    r = SESSION.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    
    # get each assignment
    for assignment in soup.find_all('tr'):
        # count for amount of details have 'a' element
        aCount = 0
        eventDate = None
        # get details of each assignment
        for details in assignment.find_all('td'):
            # only get 'a' element text from second detail that has an 'a' element
            if details.a != None:
                if aCount == 1:
                    eventName = details.a.text
                # if this detail has an 'a' element, but aCount = 0, it is the first detail with an 'a' element, but does not have the event name
                else:
                    aCount += 1
            # if detail does not have 'a' element, it has the date
            else:
                eventDate = details.text
                aCount = 0
        # add event to dictionary list
        if eventDate != None:
            assignmentDictList.append({
                'Event': eventName,
                'Date': eventDate
            })
    if assignmentDictList != []:
        return assignmentDictList
    else:
        return None
    