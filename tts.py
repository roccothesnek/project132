import pyttsx3
import pprint

engine = pyttsx3.init()

def readDueAssignments(assignments):
    ''' Must take filtered assignment list'''
    for assignment in assignments:
        engine.say(assignment)
    engine.runAndWait()
    