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


from asyncore import read
from tkinter import *
import scrape
import pyttsx3
engine = pyttsx3.init()
currentVolumeLevel = engine.getProperty('volume')
engine.setProperty('rate', 120)
engine.setProperty('volume', 0.0)
voices = engine.getProperty('voices') # we can set the voices at the beginning, 
engine.setProperty('voice', voices[0].id)




# raises the passed frame to the top visible layer
def raise_frame(frame):
    frame.tkraise()


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
root_window.columnconfigure(1, weight=12)

# Putting frames into the root window ###############
# control_frame is the frame that is always visible on the left side for switching
# between frames (aka the side buttons)
control_frame = Frame(root_window)
# The rest of the frames are displayed on the right side of the GUI after their
# button is selected.
home_frame = Frame(root_window)
calendar_frame = Frame(root_window)
alarm_frame = Frame(root_window)
login_frame = Frame(root_window)
read_frame = Frame(root_window)

# sub frame in read_frame for volume control ###############


# render each frame
# The button frame automatically spans the height of the window (even after adjustments)
# and the display frame automatically spans the height and the width.
control_frame.grid(row=0, column=0, sticky="nsew")
home_frame.grid(row=0, column=1, sticky="nsew")
calendar_frame.grid(row=0, column=1, sticky="nsew")
alarm_frame.grid(row=0, column=1, sticky="nsew")
login_frame.grid(row=0, column=1, sticky="nsew")
read_frame.grid(row=0, column=1, sticky="nsew")



##############################################


# Adding widgets to the frames ####################
# control frame widgets #########
# The buttons are placed on the left side to make them easier to tap on
readBn = Button(control_frame, text="Read",
                command=lambda: raise_frame(read_frame))
readBn.pack(side="top", fill="both", expand=1)
homeBn = Button(control_frame, text="Home",
                command=lambda: raise_frame(home_frame))
homeBn.pack(side="top", fill="both", expand=1)
calendarBn = Button(control_frame, text="Calendar",
                    command=lambda: raise_frame(calendar_frame))
calendarBn.pack(side="top", fill="both", expand=1)
alarmBn = Button(control_frame, text="Alarm",
                 command=lambda: raise_frame(alarm_frame))
alarmBn.pack(side="top", fill="both", expand=1)
loginBn = Button(control_frame, text="Login",
                 command=lambda: raise_frame(login_frame))
loginBn.pack(side="top", fill="both", expand=1)



##############################

# home frame widgets ###########
home_test = Label(home_frame, text='Home', bg='white')  # replace later
home_test.pack(side="top", fill="both", expand=1)
##############################

# calendar widgets ##############
calendar_test = Label(calendar_frame, text='Calendar', bg='white')  # replace later
calendar_test.pack(side="top", fill="both", expand=1)
#############################

# alarm frame widgets ###########
alarm_test = Label(alarm_frame, text='Alarm', bg='white')  # replace later
alarm_test.pack(side="top", fill="both", expand=1)
##############################



# login frame widgets ############
login_test = Label(login_frame, text='Login', bg='white')  # replace later
login_test.pack(side="top", fill="both", expand=1)
##############################

entry = Entry(login_frame, width = 40)
entry2 = Entry(login_frame, width = 40)
entry2.focus_set()
entry.pack()
entry.focus_set()
entry.pack()

def loginMoodle():
  global entry
  global username
  global password
  string = entry.get()
  string2 = entry2.get()
  username = string
  password = string2
  grabMoodle(username, password)
 

login_real = Button(login_frame, text = 'Login', width = 20, command = loginMoodle).pack(pady = 20)


def grabMoodle(username, password):
  #scrape.moodleLogin(username, password)
  #scrape.getMoodleAssignments()
  return 'purple'

username = 'hello'
password = 'goodbye'

def readStuff():
  engine.say(read_test['text'])
  return

# read frame widgets #############
read_test = Label(read_frame, text= 'lame', bg='white')  # replace later
read_test.pack(side="top", fill="both", expand=1)

def changeColor():
  engine.say(read_test['text'])
  return

read_actual = Button(read_frame, text="Press to read aloud",
                      command= changeColor)
read_actual.pack(side="right", fill="y", expand=3)



# volume frame widgets ###########
# all the volume shit


def volume_up():
  global currentVolumeLevel
  currentVolumeLevel += 0.1
  engine.setProperty('volume', currentVolumeLevel)
  volume = engine.getProperty('volume')
  volume_test['text'] = f'Volume is now: {volume}'
  return

def volume_down():
  global currentVolumeLevel
  currentVolumeLevel -= 0.1
  engine.setProperty('volume', currentVolumeLevel)
  volume = engine.getProperty('volume')
  volume_test['text'] = f'Volume is now: {volume}'
  return

volumeBn = Button(control_frame, text="Volume",
                  command=lambda: raise_frame(volume_frame))
volumeBn.pack(side="top", fill="both", expand=1)

volume_frame = Frame(root_window)
volume_frame.grid(row=0, column=1, sticky="nsew")

vDown = Frame(root_window)
vDown.grid(row=0, column=1, sticky="nsew")

vUp = Frame(root_window)
vUp.grid(row=0, column=1, sticky="nsew")


volume_test = Label(volume_frame, text=f'The current volume is: {currentVolumeLevel}', bg='white')  # replace later
volume_test.pack(side="top", fill="both", expand=1)



volume_up = Button(volume_frame, text="Volume Up",
                   command= volume_up)
volume_up.pack(side="top", fill="both", expand=1)

volume_down = Button(volume_frame, text="Volume Down",
                    command= volume_down)
volume_down.pack(side="top", fill="both", expand=1)

# all the read control shit


################################################

# main ####
raise_frame(home_frame)  # show the home frame on startup
root_window.mainloop()

