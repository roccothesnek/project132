from pygame import mixer


def play_alarm(file_string):
    mixer.init() # initialize pygame mixer
    mixer.music.load(file_string) # load alarm file
    mixer.music.play(-1)  # Plays the alarm. -1 parameter plays it on repeat


def stop_alarm():
    mixer.music.stop()

    