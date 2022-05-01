from tkinter.ttk import *
from tkinter import *
import time
import scrape
import pyttsx3
import threading
import alarm


# raises the passed frame to the top visible layer
def raise_frame(frame):
    frame.tkraise()


# set the time when user confirms it
def setTime():
    global ALARM_TIME
    minBuffer = ""
    if int(currentMinute.get()) < 10:
        minBuffer = "0"
    # if the meridiem is PM, add 12 hours
    if currentMeridiem.get() == "AM":
        if currentHour.get() != "12":
            ALARM_TIME = currentHour.get() + " " + currentMinute.get()
            svdTimeLabel.config(text="Alarm Time: " + currentHour.get() + ":" + minBuffer + currentMinute.get() + " AM")
        else:
            ALARM_TIME = str(int(currentHour.get()) - 12) + " " + currentMinute.get()
            svdTimeLabel.config(text="Alarm Time: " + currentHour.get() + ":" + minBuffer + currentMinute.get() + " AM")
    else:
        if currentHour.get() != "12":
            ALARM_TIME = str(int(currentHour.get()) + 12) + " " + currentMinute.get()
            svdTimeLabel.config(text="Alarm Time: " + currentHour.get() + ":" + minBuffer + currentMinute.get() + " PM")
        else:
            ALARM_TIME = currentHour.get() + " " + currentMinute.get()
            svdTimeLabel.config(text="Alarm Time: " + currentHour.get() + ":" + minBuffer + currentMinute.get() + " PM")


# set the credentials when the user confirms it
def setCredentials():
    global USERNAME
    global PASSWORD
    USERNAME = usernameBox.get()
    PASSWORD = passwordBox.get()
    # clean up credentials
    USERNAME = USERNAME.strip()
    PASSWORD = PASSWORD.strip()


# takes unfiltered assignment list, and filters them based of if the type of assignment
def filterAssignments(assignments):
    filteredAssignments = []
    assignmentCount = 0
    for assignment in assignments:
        assignmentCount += 1
        if (assignment["Event"].endswith("closes") or assignment["Event"].endswith("is due")):
            if "Tomorrow" in assignment["Date"]:
                filteredAssignments.append(
                    assignment["Event"] + " " + assignment["Date"] + " in " + assignment["Class"])
            else:
                filteredAssignments.append(
                    assignment["Event"] + " on " + assignment["Date"] + " in " + assignment["Class"])
        if assignmentCount == 6:
            break
    return filteredAssignments


# reads out assignments, must take filtered STRING of assignments
def readDueAssignments(assignments):
    # disable sliders so they dont interfere with voice
    volumeS.config(state='disabled')
    rateS.config(state='disabled')
    print(assignments)
    engine.say(assignments)
    engine.runAndWait()
    # enable sliders again
    volumeS.config(state='normal')
    rateS.config(state='normal')


# puts the 'show assignments' button on top
def raise_show_assignment_button():
    displayAssignmentsBn.place(x=760, y=0, height=40, width=40)
    clearAssignmentsBn.place_forget()


# puts the 'hide assignments' button on top
def raise_clear_assignments_button():
    clearAssignmentsBn.place(x=760, y=0, height=40, width=40)
    displayAssignmentsBn.place_forget()


# simply clears the assignment label
def clearAssignments():
    raise_show_assignment_button()
    assignmentsLabel.config(text="")


def show_loading():
    assignmentsLabel.config(text="Loading...")
    root_window.update()


# gets and displays the moodle assignments
# also hides the buttons used to turn off the alarm
def displayAssignments(readAssignments):
    show_loading()
    raise_clear_assignments_button()
    # hide the buttons used to turn off the alarm
    stopAlarmBn1.place_forget()
    stopAlarmBn2.place_forget()
    root_window.update()
    # see if user even entered credentials, if so get the assignments
    if USERNAME != None and PASSWORD != None:
        print("attempting to log in with " + USERNAME + ", " + PASSWORD)
        scrape.moodleLogin(USERNAME, PASSWORD)
        unfilteredAssignments = scrape.getMoodleAssignments()
        # see if there are any upcoming assignments
        if unfilteredAssignments != None:
            filteredAssignments = filterAssignments(unfilteredAssignments)
            assignments = ""
            # create string of assignments
            assignmentCount = 1
            for assignment in filteredAssignments:
                # splices the assignment string based off length
                if len(assignment) < 70:
                    assignments += str(assignmentCount) + ". " + assignment + "\n\n"
                    assignmentCount += 1
                else:
                    startingIndex = 70
                    index = 0
                    # looks for a space to start a new line
                    for char in range(startingIndex, len(assignment)):
                        if assignment[char] == " ":
                            assignments += str(assignmentCount) + ". " + assignment[
                                                                         0:startingIndex + index] + "\n" + assignment[
                                                                                                           startingIndex + index:len(
                                                                                                               assignment)] + "\n\n"
                            break
                        index += 1
                    assignmentCount += 1
                if assignmentCount == 6:
                    break
            # display them
            assignmentsLabel.config(text=assignments)
            if readAssignments == True:
                # create a single readable string of assignments
                readAssignmentString = "Hello, your upcoming assignments are: "
                for assignment in filteredAssignments:
                    readAssignmentString += assignment
                # ceate and execute new thread so the GUI doesn't stop responding
                thread = threading.Thread(target=readDueAssignments, args=(readAssignmentString,))
                thread.start()
            print("ASSIGNMENTS: " + assignments)
        else:
            assignmentsLabel.config(text="Your credentials may be incorrect or you have no assignments.")
    else:
        assignmentsLabel.config(text="No submitted credentials")


def clockTime():
    textTime = time.strftime("%H:%M")
    hourTime = int(textTime[0:2])
    if hourTime > 12:
        hourTime -= 12
        hourTime = str(hourTime)
        timeLabel.config(text=hourTime + textTime[2:len(textTime)] + " PM")
    elif hourTime == 0:
        hourTime += 12
        hourTime = str(hourTime)
        timeLabel.config(text=hourTime + textTime[2:len(textTime)] + " AM")
    else:
        timeLabel.config(text=textTime + " AM")
    timeLabel.after(200, clockTime)


# user input
ALARM_TIME = None
USERNAME = None
PASSWORD = None

# widget constants
BACKGROUND_COLOR = '#232429'
TEXT_COLOR = "white"
FONT = 'Calibri'
BUTTON_COLOR = "#1c5ffe"
FIELD_COLOR = "#333742"
BORDERWIDTH = 0

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
root_window.rowconfigure(0, weight=1)
# adjusting the weights of the next two methods will change the control frame (side
# button) width
root_window.columnconfigure(0, weight=1)

# Putting frames into the root window ###############
# control_frame is the frame that leds the user configure the alarm settings
control_frame = Frame(root_window, bg=BACKGROUND_COLOR)
# home_frame is the home frame
home_frame = Frame(root_window, bg=BACKGROUND_COLOR)
# speak frame
speak_frame = Frame(root_window, bg=BACKGROUND_COLOR)
# render each frame
control_frame.grid(row=0, column=0, sticky="nsew")
home_frame.grid(row=0, column=0, sticky="nsew")
speak_frame.grid(row=0, column=0, sticky="nsew")
##############################################


# Adding widgets to the frames ####################
####### Home Frame Widgets #######
# button that takes user to control_frame
settingsPhoto = PhotoImage(file='settings_icon.gif')
settingsBn = Button(home_frame, image=settingsPhoto, command=lambda: raise_frame(control_frame), bd=BORDERWIDTH)
settingsBn.place(x=0, y=0, height=60, width=60)

# Displays current time
timeLabel = Label(home_frame, fg=TEXT_COLOR, font=(FONT, 70, 'bold'), text="12:38 PM", bg=BACKGROUND_COLOR)
timeLabel.place(x=220, y=50, height=100, width=360)

# button to display and read assignments
readAssignmentsPhoto = PhotoImage(file='play_icon.gif')
readAssignmentsBn = Button(home_frame,
                           image=readAssignmentsPhoto,
                           command=lambda: displayAssignments(True), bd=BORDERWIDTH)
readAssignmentsBn.place(x=760, y=40, height=40, width=40)

# display assignments button
displayAssignmentsPhoto = PhotoImage(file='show_icon.gif')
displayAssignmentsBn = Button(home_frame, text="Clear Assignments", image=displayAssignmentsPhoto,
                              command=lambda: displayAssignments(False), bd=BORDERWIDTH)
displayAssignmentsBn.place(x=760, y=0, height=40, width=40)

# clear button
clearAssignmentsPhoto = PhotoImage(file='clear_icon.gif')
clearAssignmentsBn = Button(home_frame, image=clearAssignmentsPhoto,
                            command=lambda: clearAssignments(), bd=BORDERWIDTH)

# sets clock label to correct time
clockTime()

# Assignments Label
assignmentsLabel = Label(home_frame, font=(FONT, 13), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
assignmentsLabel.place(x=75, y=150, height=300, width=650)

# Loading Bar
loadingBar = Progressbar(home_frame, orient=HORIZONTAL, length=100, mode='indeterminate')

# Button to turn off alarm and only display assignments
stopAlarmBn1 = Button(home_frame, text="Only Display Assignments",
                      font=(FONT, 15), fg=TEXT_COLOR, bg=BUTTON_COLOR,
                      command=lambda: [alarm.stop_alarm(), displayAssignments(False)])

# Button to turn off alarm and both display and read assignments
stopAlarmBn2 = Button(home_frame, text="Display and Read Assignments",
                      font=(FONT, 15), fg=TEXT_COLOR, bg=BUTTON_COLOR,
                      command=lambda: [alarm.stop_alarm(), show_loading(), displayAssignments(True)])
#####################################

####### Control Frame Widgets #######
# takes user back to home_frame
homePhoto = PhotoImage(file='home_icon.gif')
homeBn = Button(control_frame, command=lambda: raise_frame(home_frame), image=homePhoto, bd=BORDERWIDTH)
homeBn.place(x=0, y=0, height=60, width=60)

# button to show speak frame
speakBn = Button(control_frame, text="Sound Settings", font=(FONT, 18), fg=TEXT_COLOR, bg=BUTTON_COLOR,
                 command=lambda: raise_frame(speak_frame))
speakBn.place(x=600, y=0, height=40, width=200)

# sets the input for the time the user specified
alarmSetBn = Button(control_frame, bg=BUTTON_COLOR, fg=TEXT_COLOR, text="Set Alarm", font=(FONT, 20),
                    command=lambda: setTime(), bd=BORDERWIDTH)
alarmSetBn.place(x=300, y=150, height=50, width=200)

# lets user see saved time
svdTimeLabel = Label(control_frame, fg=TEXT_COLOR, text="Alarm Time: None", font=(FONT, 35), bg=BACKGROUND_COLOR)
svdTimeLabel.place(x=150, y=40, height=50, width=500)

# lets user set the hour with a spin box
hourLabel = Label(control_frame, fg=TEXT_COLOR, text="Hour:", font=(FONT, 25), bg=BACKGROUND_COLOR)
hourLabel.place(x=100, y=100, height=40, width=75)
currentHour = StringVar(value=1)
hourSpin = Spinbox(control_frame, from_=1, to=12, textvariable=currentHour, wrap=True, readonlybackground=FIELD_COLOR,
                   fg=TEXT_COLOR, bd=BORDERWIDTH, font=(FONT, 25), buttonbackground=BUTTON_COLOR, state='readonly')
hourSpin.place(x=180, y=100, height=40, width=80)

# lets user set the minute with a spin box
minuteLabel = Label(control_frame, text="Minute:", font=(FONT, 25), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
minuteLabel.place(x=280, y=100, height=40, width=110)
currentMinute = StringVar(value=0)
minuteSpin = Spinbox(control_frame, from_=0, to=59, textvariable=currentMinute, wrap=True, state='readonly',
                     readonlybackground=FIELD_COLOR, fg=TEXT_COLOR, bd=BORDERWIDTH, font=(FONT, 25),
                     buttonbackground=BUTTON_COLOR)
minuteSpin.place(x=395, y=100, height=40, width=80)

# lets user set the meridiem with a dropdown box
meridiemLabel = Label(control_frame, text="Meridiem:", font=(FONT, 25), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
meridiemLabel.place(x=500, y=100, height=40, width=140)
meridiemOptions = ["AM", "PM"]
currentMeridiem = StringVar(value="AM")
meridiemDropDown = OptionMenu(control_frame, currentMeridiem, *meridiemOptions)
meridiemDropDown.config(bg=FIELD_COLOR, fg=TEXT_COLOR, bd=BORDERWIDTH, activebackground=BUTTON_COLOR,
                        activeforeground=TEXT_COLOR)
meridiemDropDown["menu"].config(bg=FIELD_COLOR, fg=TEXT_COLOR, bd=BORDERWIDTH, activebackground=BUTTON_COLOR)
meridiemDropDown.place(x=645, y=100, height=40, width=75)

# sets the input for the credentials the user specified
loginSetBn = Button(control_frame, text="Save Credentials", font=(FONT, 20), bg=BUTTON_COLOR, fg=TEXT_COLOR,
                    bd=BORDERWIDTH, command=lambda: setCredentials())
loginSetBn.place(x=300, y=350, height=50, width=200)

# lets the user enter their username and password into a text box
credentialsLabel = Label(control_frame, text="Moodle Credentials", font=(FONT, 35), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
credentialsLabel.place(x=150, y=240, height=50, width=500)
usernameLabel = Label(control_frame, text="Username:", font=(FONT, 25), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
usernameLabel.place(x=100, y=300, height=40, width=140)
usernameBox = Entry(control_frame, fg=TEXT_COLOR, bg=FIELD_COLOR, font=(FONT, 25), bd=BORDERWIDTH)
usernameBox.place(x=245, y=300, height=40, width=140)
passwordLabel = Label(control_frame, text="Password:", fg=TEXT_COLOR, bg=BACKGROUND_COLOR, font=(FONT, 25))
passwordLabel.place(x=400, y=300, height=40, width=140)
passwordBox = Entry(control_frame, show="*", font=(FONT, 25), bg=FIELD_COLOR, fg=TEXT_COLOR, bd=BORDERWIDTH)
passwordBox.place(x=545, y=300, height=40, width=140)

## speak frame
volumeL = Label(speak_frame, text="Volume:", font=(FONT, 35), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
volumeL.place(x=200, y=80, height=60, width=180)


# function to set the volume of the pyttsx3 engine
def setVolume(volume):
    volume = int(volume)
    volume = volume / 100
    print(volume)
    engine.setProperty('volume', volume)
    engine.runAndWait()


# adds a slider to adjust the volume
volumeS = Scale(speak_frame, from_=0, to=100, orient=HORIZONTAL, bg=FIELD_COLOR, fg=TEXT_COLOR, bd=BORDERWIDTH,
                font=(FONT, 25), length=200, command=lambda x: setVolume(x))
volumeS.place(x=380, y=80, height=60, width=150)

# rate label
rateL = Label(speak_frame, text="Rate of Speech:", font=(FONT, 35), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
rateL.place(x=90, y=200, height=60, width=300)

rateLFast = Label(speak_frame, text="Fast", font=(FONT, 12), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
rateLFast.place(x=490, y=200, height=20, width=100)

rateLNormal = Label(speak_frame, text=" Normal", font=(FONT, 12), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
rateLNormal.place(x=420, y=200, height=20, width=100)

rateLSlow = Label(speak_frame, text=" Slow", font=(FONT, 12), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
rateLSlow.place(x=380, y=200, height=20, width=70)


# function to set rate of the pyttsx3 engine
def setRate(rate):
    rate = int(rate)
    rate = rate
    engine.setProperty('rate', rate)
    engine.runAndWait()


# adds a slider to adjust the rate
rateS = Scale(speak_frame, from_=0, to=200, orient=HORIZONTAL, showvalue=0, bg=FIELD_COLOR, fg=TEXT_COLOR,
              bd=BORDERWIDTH, font=(FONT, 25), length=200, command=lambda x: setRate(x))
rateS.place(x=400, y=220, height=20, width=150)

homeBnSpk = Button(speak_frame, image=homePhoto, bg=BUTTON_COLOR, bd=BORDERWIDTH,
                   command=lambda: raise_frame(home_frame))
homeBnSpk.place(x=0, y=0, height=60, width=60)

settingsBnSpk = Button(speak_frame, image=settingsPhoto, bg=BUTTON_COLOR, bd=BORDERWIDTH,
                       command=lambda: raise_frame(control_frame))
settingsBnSpk.place(x=735, y=0, height=60, width=60)

# pick alarm sounds from dropdown menu
alarmSoundLabel = Label(speak_frame, text="Alarm Sound:", font=(FONT, 25), fg=TEXT_COLOR, bg=BACKGROUND_COLOR)
alarmSoundLabel.place(x=200, y=320, height=40, width=180)

alarmSoundOptions = ["Samsung.mp3", "Doom.mp3", "Nujabes.m4a", "wakeup_chill_alarm.mp3"]
currentAlarmSound = StringVar(value="Samsung.mp3")

alarmSoundDropDown = OptionMenu(speak_frame, currentAlarmSound, *alarmSoundOptions)
alarmSoundDropDown.config(bg=FIELD_COLOR, fg=TEXT_COLOR, bd=BORDERWIDTH, activebackground=BUTTON_COLOR)
alarmSoundDropDown["menu"].config(bg=FIELD_COLOR, fg=TEXT_COLOR, bd=BORDERWIDTH, activebackground=BUTTON_COLOR)
alarmSoundDropDown.place(x=400, y=320, height=40, width=140)


####################################

# the main operation
def main():
    global ALARM_TIME
    global USERNAME
    global PASSWORD
    global assignmentLabel
    # first see if an alarm has even been set
    if ALARM_TIME != None:
        # get hour and minute separately
        hrMin = ALARM_TIME.split()
        # see if the current time matches the set alarm time
        if int(hrMin[0]) == int(time.strftime("%H")) and int(hrMin[1]) == int(time.strftime("%M")):
            clearAssignments()
            raise_frame(home_frame)
            AlarmSound = currentAlarmSound.get()
            # sound the alarm
            alarm.play_alarm(AlarmSound)
            # display the buttons to stop the alarm
            stopAlarmBn1.place(x=75, y=180, height=200, width=325)
            stopAlarmBn2.place(x=400, y=180, height=200, width=325)
            # reset alarm time
            ALARM_TIME = None
            svdTimeLabel.config(text="Alarm Time: None")
    # recurse
    root_window.after(1000, main)

raise_frame(home_frame)  # show the home frame on startup
main()
root_window.mainloop()
