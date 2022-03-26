import requests
from bs4 import BeautifulSoup

SESSION = requests.Session()

def login(username, password):
    ''' Simply logs in the session, takes 2 strings for username and password, this must be called before scraping assignments '''
    
    # payload for login POST request
    login_data = {
        'username': username,
        'password': password,
        '_eventId': 'submit',
        'geolocation': ''
    }       
    
    # go to login page
    url = "https://cas.latech.edu/cas/login?service=https%3A%2F%2Fmoodle.latech.edu%2Flogin%2Findex.php"
    r = SESSION.get(url)
    # use bs to find hidden title "execution" value and attach to payload
    soup = BeautifulSoup(r.content, 'html5lib')
    login_data['execution'] = soup.find('input', attrs={'name': 'execution'})['value']
    # send post request to log in
    r = SESSION.post(url, data = login_data)
    
def getAssignments():
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
    return assignmentDictList
