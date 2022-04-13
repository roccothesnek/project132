# Import the library tkinter
from tkinter import *

# Create a GUI app
window = Tk()
window.geometry("800x500")

window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)

# individual names
homeWindow = Frame(window)
settingsWindow = Frame(window)

# render each frames
for frame in (homeWindow, settingsWindow):
    frame.grid(row = 0, column = 0, sticky = 'nsew')

# raises the passed frame to the top visible layer
def raiseFrame(frame):
    frame.tkraise()

# homeWindow elements
homeTitle = Label(homeWindow, text = 'Home', bg = 'white')
homeTitle.pack(fill = 'both', expand = True)
settingsBn = Button(homeWindow, text = "Settings", command = lambda:raiseFrame(settingsWindow))
settingsBn.pack(fill = 'x', ipady = 15)

# settigns window elements
settingsTitle = Label(settingsWindow, text = 'Settings', bg = 'white')
settingsTitle.pack(fill = 'both', expand = True)
homeBtn = Button(settingsWindow, text = "Home", command = lambda:raiseFrame(homeWindow))
homeBtn.pack(fill = 'x', ipady = 15)

raiseFrame(homeWindow)
window.mainloop()
