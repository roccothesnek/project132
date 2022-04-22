import scrape
import tts
import time

def filterAssignments(assignments):
    filteredAssignments = []
    
    for assignment in assignments:
        if (assignment["Event"].endswith("closes") or assignment["Event"].endswith("is due")):
            if "Tomorrow" in assignment["Date"]:
                filteredAssignments.append(assignment["Event"] + " " + assignment["Date"] + " in " + assignment["Class"])
            else:
                filteredAssignments.append(assignment["Event"] + " on " + assignment["Date"] + " in " + assignment["Class"])
    
    return filteredAssignments
    
gottenAssignments = False

scrape.moodleLogin("jrf038", "Saysay12!")
unfilteredAssignments = scrape.getMoodleAssignments()
filteredAssignments = filterAssignments(unfilteredAssignments)
tts.readDueAssignments(filteredAssignments)