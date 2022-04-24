from tkinter import *
import time
import scrape
import pyttsx3
import threading

# user input
ALARM_TIME = None
USERNAME = None
PASSWORD = None

# raises the passed frame to the top visible layer
def raise_frame(frame):
    frame.tkraise()

# set the time when user confirms it
def setTime():
    global ALARM_TIME
    # if the meridiem is PM, add 12 hours
    if currentMeridiem.get() == "AM":
        if currentHour.get() != "12":
            ALARM_TIME = currentHour.get() + " " + currentMinute.get()
            svdTimeLabel.config(text = "Alarm Time: " + currentHour.get() + ":" + currentMinute.get() + " AM")
        else:
            ALARM_TIME = str(int(currentHour.get()) - 12) + " " + currentMinute.get()
            svdTimeLabel.config(text = "Alarm Time: " + currentHour.get() + ":" + currentMinute.get() + " AM")
    else:
        if currentHour.get() != "12":
            ALARM_TIME = str(int(currentHour.get()) + 12) + " " + currentMinute.get()
            svdTimeLabel.config(text = "Alarm Time: " + currentHour.get() + ":" + currentMinute.get() + " PM")
        else:
            ALARM_TIME = currentHour.get() + " " + currentMinute.get()
            svdTimeLabel.config(text = "Alarm Time: " + currentHour.get() + ":" + currentMinute.get() + " PM")

# set the credentials when the user confirms it
def setCredentials():
    global USERNAME
    global PASSWORD
    USERNAME = usernameBox.get("1.0", END)
    PASSWORD = passwordBox.get("1.0", END)
    # clean up credentials
    USERNAME = USERNAME.strip()
    PASSWORD = PASSWORD.strip()

# takes unfiltered assignment list, and filters them based of if the type of assignment
def filterAssignments(assignments):
    filteredAssignments = []
    for assignment in assignments:
        if (assignment["Event"].endswith("closes") or assignment["Event"].endswith("is due")):
            if "Tomorrow" in assignment["Date"]:
                filteredAssignments.append(assignment["Event"] + " " + assignment["Date"] + " in " + assignment["Class"])
            else:
                filteredAssignments.append(assignment["Event"] + " on " + assignment["Date"] + " in " + assignment["Class"])
    return filteredAssignments
    
# reads out assignments, must take filtered STRING of assignments
def readDueAssignments(assignments):
    engine.say(assignments)
    engine.runAndWait()

# simply clears the assignment label
def clearAssignments():
    assignmentsLabel.config(text = "")

# initialize pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# define the root_window
root_window = Tk()
# could be changed to automatically cover the whole screen when opened?
root_window.geometry("800x500")

# Divides the root window into two columns and a row.
# The weight parameter controls the size of the rows/columns by forming a ratio
# with the weight parameters for the other rows/columns.
root_window.rowconfigure(0, weight = 1)
# adjusting the weights of the next two methods will change the control frame (side
# button) width
root_window.columnconfigure(0, weight = 1)

# Putting frames into the root window ###############
# control_frame is the frame that leds the user configure the alarm settings
control_frame = Frame(root_window, bg = 'light gray')
# home_frame is the home frame
home_frame = Frame(root_window, bg = 'light gray')

# render each frame
control_frame.grid(row = 0, column = 0, sticky = "nsew")
home_frame.grid(row = 0, column = 0, sticky = "nsew")
##############################################


# Adding widgets to the frames ####################
####### Home Frame Widgets #######
# button that takes user to control_frame
settingsPhoto = PhotoImage(file = '/settings_icon.gif')
settingsBn = Button(home_frame, image = settingsPhoto, command = lambda: raise_frame(control_frame))
settingsBn.place(x = 0, y = 0, height = 40, width = 40)

# clear button
clearAssignmentsBn = Button(home_frame, text="Clear Assignments", font = ("Calibri", 15), command = lambda: clearAssignments())
clearAssignmentsBn.place(x = 620, y = 0, height = 40, width = 180)

# Displays current time
timeLabel = Label(home_frame, font = ("Calibri", 70, 'bold'), text = "12:38 PM", bg = 'light gray')
timeLabel.place(x = 220, y = 100, height = 100, width = 360)
# sets clock label to correct time
def clockTime():
    textTime = time.strftime("%H:%M")
    hourTime = int(textTime[0:2])
    if hourTime > 12:
        hourTime -= 12
        hourTime = str(hourTime)
        timeLabel.config(text = hourTime + textTime[2:len(textTime)] + " PM")
    elif hourTime == 0:
        hourTime += 12
        hourTime = str(hourTime)
        timeLabel.config(text = hourTime + textTime[2:len(textTime)] + " AM")
    else:
        timeLabel.config(text = textTime + " AM")
    timeLabel.after(200, clockTime)
clockTime()

# Assignments Label
assignmentsLabel = Label(home_frame, font = ("Calibri", 13), bg = 'light gray')
assignmentsLabel.place(x = 75 , y = 200, height = 300, width = 650)
#####################################

####### Control Frame Widgets #######
# takes user back to home_frame
homePhoto = PhotoImage(file = '/home_icon.gif')
homeBn = Button(control_frame, command=lambda: raise_frame(home_frame), image = homePhoto)
homeBn.place(x = 0, y = 0, height = 40, width = 40)

# sets the input for the time the user specified
alarmSetBn = Button(control_frame, text = "Set Alarm", font = ("Calibri", 20), command = lambda: setTime())
alarmSetBn.place(x = 300, y = 200, height = 50, width = 200)

# lets user see saved time
svdTimeLabel = Label(control_frame, text = "Alarm Time: None", font = ("Calibri", 35), bg = "light gray")
svdTimeLabel.place(x =  150, y = 90, height = 50, width = 500)

# lets user set the hour with a spin box
hourLabel = Label(control_frame, text = "Hour:", font = ("Calibri", 25), bg = 'light gray')
hourLabel.place(x = 100, y = 150, height = 40, width = 75)
currentHour = StringVar(value = 1)
hourSpin = Spinbox(control_frame, from_ = 1, to = 12, textvariable = currentHour, wrap = True, font = ("Calibri", 25))
hourSpin.place(x = 180, y = 150, height = 40, width = 80)

# lets user set the minute with a spin box
minuteLabel = Label(control_frame, text = "Minute:", font = ("Calibri", 25), bg = 'light gray')
minuteLabel.place(x = 280, y = 150, height = 40, width = 110)
currentMinute = StringVar(value = 0)
minuteSpin = Spinbox(control_frame, from_ = 0, to = 59, textvariable = currentMinute, wrap = True, font = ("Caibri", 25))
minuteSpin.place(x = 395, y = 150, height = 40, width = 80)

# lets user set the meridiem with a dropdown box
meridiemLabel = Label(control_frame, text = "Meridiem:", font = ("Calibri", 25), bg = 'light gray')
meridiemLabel.place(x =500, y = 150, height = 40, width = 140)
meridiemOptions = ["AM", "PM"]
currentMeridiem = StringVar(value = "AM")
meridiemDropDown = OptionMenu(control_frame, currentMeridiem, *meridiemOptions)
meridiemDropDown.place(x = 645, y = 150, height = 40, width = 75)

# sets the input for the credentials the user specified
loginSetBn = Button(control_frame, text = "Save Credentials", font = ("Calibri", 20), command = lambda: setCredentials())
loginSetBn.place(x = 300, y = 400, height = 50, width = 200)

# lets the user enter their username and password into a text box
credentialsLabel = Label(control_frame, text = "Moodle Credentials", font = ("Calibri", 35), bg = 'light gray')
credentialsLabel.place(x = 150, y = 290, height = 50, width = 500)
usernameLabel = Label(control_frame, text = "Username:", font = ("Calibri", 25), bg = 'light gray')
usernameLabel.place(x = 100, y = 350, height = 40, width = 140)
usernameBox = Text(control_frame, font = ("Calibri", 25))
usernameBox.place(x = 245, y = 350, height = 40, width = 140)
passwordLabel = Label(control_frame, text = "Password:", font = ("Calibri", 25), bg = 'light gray')
passwordLabel.place(x = 400, y = 350, height = 40, width = 140)
passwordBox = Text(control_frame, font = ("Calibri", 25))
passwordBox.place(x = 545, y = 350, height = 40, width = 140)
####################################

# the main operation
def main():
    global ALARM_TIME
    global USERNAME
    global PASSWORD
    # first see if an alarm has even been set
    if ALARM_TIME != None:
        # get hour and minute separately
        hrMin = ALARM_TIME.split()
        # see if the current time matches the set alarm time
        if int(hrMin[0]) == int(time.strftime("%H")) and int(hrMin[1]) == int(time.strftime("%M")):
            # see if user even entered credentials, if so get the assignments
            if USERNAME != None and PASSWORD != None:
                print("attempting to log in with " + USERNAME + ", " + PASSWORD)
                scrape.moodleLogin(USERNAME, PASSWORD)
                unfilteredAssignments = scrape.getMoodleAssignments()
                filteredAssignments = filterAssignments(unfilteredAssignments)
                # see if there are any upcoming assignments
                if filteredAssignments != None:
                    assignments = ""
                    # create string of assignments
                    assignmentCount = 1
                    for assignment in filteredAssignments:
                        # spplices the assignment string based off length
                        if len(assignment) < 90:
                            assignments += str(assignmentCount) + ". " + assignment + "\n\n"
                            assignmentCount += 1
                        else:
                            startingIndex = 70
                            index = 0
                            # looks for a space to start a new line
                            for char in range(startingIndex, len(assignment)):
                                if assignment[char] == " ":
                                    assignments += str(assignmentCount) + ". " + assignment[0:startingIndex + index] + "\n" + assignment[startingIndex + index:len(assignment)] + "\n\n"
                                    break
                                index += 1
                            assignmentCount += 1
                        if assignmentCount == 6:
                            break
                    # display them
                    assignmentsLabel.config(text = assignments)
                    # create a single readable string of assignments
                    readAssignmentString = "Hello, your upcoming assignments are: "
                    for assignment in filteredAssignments:
                        readAssignmentString += assignment
                    # create and execute new thread so the GUI doesn't stop responding
                    ttsThread = threading.Thread(target = readDueAssignments, args = (readAssignmentString,))
                    ttsThread.start()
                    print("ASSIGNMENTS: " + assignments)
            # reset alarm time
            ALARM_TIME = None
            svdTimeLabel.config(text = "Alarm Time: None")
    # recurse
    root_window.after(1000, main)
    
raise_frame(home_frame)  # show the home frame on startup
main()
root_window.mainloop()