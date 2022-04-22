####################################################################
# Description: Creates a tkinter window with a small control frame to the left and
# a larger frame to the right. The larger frame will be used for various functions
# such as setting an alarm, choosing days on a calendar, logging into Moodle, etc.
# The smaller frame is always present and is composed of buttons to choose what
# the main frame is displaying.
###################################################################

# ideas for improvement ############
# - put icons on buttons
# - make it so that the GUI covers the whole screen upon opening
################################


from tkinter import *
import time

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
    if currentMeridiem.get() == "AM":
        ALARM_TIME = currentHour.get() + " " + currentMinute.get()
    else:
        ALARM_TIME = str(int(currentHour.get()) + 12) + " " + currentMinute.get()
    
    print(ALARM_TIME)

# set the credentials when the user confirms it
def setCredentials():
    global USERNAME
    global PASSWORD
    USERNAME = usernameBox.get("1.0", END)
    PASSWORD = passwordBox.get("1.0", END)
    print(USERNAME)
    print(PASSWORD)

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
control_frame = Frame(root_window, bg = 'light gray')
# home_frame is the home frame
home_frame = Frame(root_window, bg = 'light gray')

# render each frame
control_frame.grid(row = 0, column = 0, sticky="nsew")
home_frame.grid(row = 0, column = 0, sticky="nsew")
##############################################


# Adding widgets to the frames ####################
####### Home Frame Widgets #######
# button that takes user to control_frame
settingsPhoto = PhotoImage(file = 'C:/Users/jadyn/Desktop/New folder/project132/settings_icon.gif')
settingsBn = Button(home_frame, image = settingsPhoto, command = lambda: raise_frame(control_frame))
settingsBn.place(x = 0, y = 0, height = 40, width = 40)

# read button
readBn = Button(home_frame, text="Read")
readBn.place(x = 500, y = 300, height = 40, width = 100)

# Displays current time
timeLabel = Label(home_frame, font = ("Calibri", 70, 'bold'), text = "09:38", bg = 'light gray')
timeLabel.place(x = 250, y = 100, height = 100, width = 300)
def clockTime():
    textTime = time.strftime("%H:%M")
    hourTime = int(textTime[0:2])
    if hourTime > 12:
        hourTime -= 12
        hourTime = str(hourTime)
        timeLabel.config(text = hourTime + textTime[2:len(textTime)])
    else:
        timeLabel.config(text = textTime)
    timeLabel.after(200, clockTime)
clockTime()
#####################################

####### Control Frame Widgets #######
# takes user back to home_frame
homePhoto = PhotoImage(file = 'C:/Users/jadyn/Desktop/New folder/project132/home_icon.gif')
homeBn = Button(control_frame, command=lambda: raise_frame(home_frame), image = homePhoto)
homeBn.place(x = 0, y = 0, height = 40, width = 40)

# sets the input for the time the user specified
alarmSetBn = Button(control_frame, text = "Set Alarm", font = ("Calibri", 20), command = lambda: setTime())
alarmSetBn.place(x = 300, y = 200, height = 50, width = 200)

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
minuteSpin = Spinbox(control_frame, from_ = 0, to = 60, textvariable = currentMinute, wrap = True, font = ("Caibri", 25))
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
usernameLabel = Label(control_frame, text = "Username:", font = ("Calibri", 25), bg = 'light gray')
usernameLabel.place(x = 100, y = 350, height = 40, width = 140)
usernameBox = Text(control_frame, font = ("Calibri", 25))
usernameBox.place(x = 245, y = 350, height = 40, width = 140)
passwordLabel = Label(control_frame, text = "Password:", font = ("Calibri", 25), bg = 'light gray')
passwordLabel.place(x = 400, y = 350, height = 40, width = 140)
passwordBox = Text(control_frame, font = ("Calibri", 25))
passwordBox.place(x = 545, y = 350, height = 40, width = 140)
####################################

# main ####
raise_frame(home_frame)  # show the home frame on startup
root_window.mainloop()
