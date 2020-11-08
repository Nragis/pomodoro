from tkinter import *
from tkinter import ttk
import random as random
import time as t

class pomodoro:
    def __init__(self, parent):
        # Initializing Variables
        self.pomodoroLength = 25
        self.shortBreakLength = 1
        self.longBreakLength = 15
        self.pomodorosInGroup = 4
        self.pomodoroCount = 0
        self.timerSec = self.pomodoroLength*60

        self.timeRan = 0
        self.initialStartTime = 0

        self.timerOn = False
        self.autoplay = True
        self.settingsOpen = False
        self.timerState = 'POMODORO'
        self.notificationSound = ''

        # Initializing mainframe and title
        self.parent = parent
        root.title("Pomodoro Timer")

        # Initializing Styles
        self.s = ttk.Style()
        self.s.theme_use('clam')
        self.s.configure('.')
        self.s.map('.', highlightcolor=[], foreground=[], background=[('disabled', '#d9d9d9'), ('active', '#ececec')])

        self.s.configure('TimerFrame.TFrame', background='tomato')
        self.s.configure('TimerFrame.TLabel', background='tomato')
        self.s.configure('TimerFrame.TButton', background='tomato', highlightthickness=0)
        self.s.map('TimerFrame.TButton',background=[('active', 'light coral'),('pressed', 'coral')])

        self.s.configure('Timer.TimerFrame.TLabel', font=('',72))

        self.s.configure('TaskFrame.TFrame', background='grey')

        # Creating mainframe
        self.mainframe = ttk.Frame(parent)
        self.mainframe.grid(row=0,column=0,sticky="N E S W")

        # Creating and placing containers
        self.timerFrame = ttk.Frame(self.mainframe, style='TimerFrame.TFrame',height=100,width=100)
        self.taskFrame = ttk.Frame(self.mainframe, style='TaskFrame.TFrame',height=100,width=100)
        self.doneFrame = ttk.Frame(self.mainframe)

        self.timerFrame.grid(row=0,column=0,sticky='N E S W')
        self.taskFrame.grid(row=1,column=0,sticky='N E S W')
        self.doneFrame.grid(row=2,column=0,sticky='N E S W')

        # Creating and placing timerFrame widgets
        self.timerLabelVar = StringVar(); self.timerLabelVar.set("{}:00".format(self.pomodoroLength))
        self.focusLabelVar = StringVar(); self.focusLabelVar.set("100% Focus")
        self.pomodoroCountLabelVar = StringVar(); self.pomodoroCountLabelVar.set("1 (1)")

        self.settingsButton = ttk.Button(self.timerFrame, text='Settings', style='TimerFrame.TButton', command=self.open_settings)
        self.resetButton= ttk.Button(self.timerFrame, text='Reset', style='TimerFrame.TButton', command=self.reset_timer)
        self.startstopButton= ttk.Button(self.timerFrame, text='Start Timer', style='TimerFrame.TButton', command=self.start_timer)
        self.skipButton = ttk.Button(self.timerFrame, text='Skip', style='TimerFrame.TButton', command=self.skip_timer)
        self.timerLabel = ttk.Label(self.timerFrame, textvariable=self.timerLabelVar, style='Timer.TimerFrame.TLabel')
        self.focusLabel = ttk.Label(self.timerFrame, textvariable=self.focusLabelVar, style='TimerFrame.TLabel')
        self.pomodoroCountLabel = ttk.Label(self.timerFrame, textvariable=self.pomodoroCountLabelVar, style='TimerFrame.TLabel')

        self.settingsButton.grid(row=0,column=0,sticky='NW')
        self.resetButton.grid(row=3,column=0,sticky='SW')
        self.startstopButton.grid(row=2,column=1,sticky="E", padx=(0,25))
        self.skipButton.grid(row=2,column=2,sticky="W", padx=(25,0))
        self.timerLabel.grid(row=1,column=1,columnspan=2)
        self.focusLabel.grid(row=3,column=3,sticky='SE')
        self.pomodoroCountLabel.grid(row=0,column=3,sticky='NE')

        # row/column configure
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.rowconfigure(2, weight=1)

        self.timerFrame.columnconfigure(0, weight=1,minsize=100)
        self.timerFrame.columnconfigure(1, weight=5,minsize=100)
        self.timerFrame.columnconfigure(2, weight=5,minsize=100)
        self.timerFrame.columnconfigure(3, weight=1,minsize=100)
        self.timerFrame.rowconfigure(0, weight=1)
        self.timerFrame.rowconfigure(1, weight=5)
        self.timerFrame.rowconfigure(2, weight=5)
        self.timerFrame.rowconfigure(3, weight=1)

    def reset_timer(self):
        self.timerOn = False
        self.timerSec = self.pomodoroLength*60
        self.startstopButton.configure(text='Start Timer', command=self.start_timer)
        self.timerLabelVar.set("{}:00".format(self.pomodoroLength))
        self.pomodoroCount = 0
        self.pomodoroCountLabelVar.set("{}({})".format(int(self.pomodoroCount/self.pomodorosInGroup) + 1, self.pomodoroCount%self.pomodorosInGroup + 1))
        self.timeRan = 0
        self.initialStartTime= 0
        self.focusLabelVar.set("100% Focus")

    def open_settings(self):
        #helper functions
        def close_window():
            self.settingsOpen = False
            self.settingsWindow.destroy()
            self.settingsWindow.update()
            self.settingsWindow = None

        def save_settings():
            self.pomodoroLength = int(pomodoroLength.get())
            self.shortBreakLength = int(shortBreakLength.get())
            self.longBreakLength = int(longBreakLength.get())
            self.pomodorosInGroup = int(pomodorosInGroup.get())
            self.autoplay = False if autoplay.get() == 'F' else True
            self.notificationSound = notificationSound.get()
            self.reset_timer()
            close_window()

        if self.settingsOpen: close_window()
        self.settingsOpen = True
        self.settingsWindow = Toplevel(self.parent)
        self.settingsWindow.title("Settings")
        self.settingsWindow.resizable(False, False)

        # Creating mainframe
        self.settingsMainframe = ttk.Frame(self.settingsWindow)
        self.settingsMainframe.grid(row=0,column=0,sticky="N E S W")

        # Creating and placing timerFrame widgets
        ttk.Label(self.settingsMainframe, text='Pomodoro Length').grid(row=0,column=0,sticky="W")
        ttk.Label(self.settingsMainframe, text='Short Break Length').grid(row=1,column=0,sticky="W")
        ttk.Label(self.settingsMainframe, text='Long Break Length').grid(row=2,column=0,sticky="W")
        ttk.Label(self.settingsMainframe, text='Pomodoro\'s in Group').grid(row=3,column=0,sticky="W")
        ttk.Label(self.settingsMainframe, text='Autoplay').grid(row=4,column=0,sticky="W")
        ttk.Label(self.settingsMainframe, text='Notification Sound').grid(row=5,column=0,sticky="W")

        pomodoroLength = StringVar()
        shortBreakLength = StringVar()
        longBreakLength = StringVar()
        pomodorosInGroup = StringVar()
        autoplay = StringVar()
        notificationSound = StringVar()

        ttk.Spinbox(self.settingsMainframe, from_=1, to=120, textvariable=pomodoroLength).grid(row=0,column=1)
        ttk.Spinbox(self.settingsMainframe, from_=1, to=30, textvariable=shortBreakLength).grid(row=1,column=1)
        ttk.Spinbox(self.settingsMainframe, from_=1, to=60, textvariable=longBreakLength).grid(row=2,column=1)
        ttk.Spinbox(self.settingsMainframe, from_=1, to=8, textvariable=pomodorosInGroup).grid(row=3,column=1)
        ttk.Checkbutton(self.settingsMainframe, variable=autoplay, onvalue='T', offvalue='F').grid(row=4,column=1)
        ttk.Combobox(self.settingsMainframe, textvariable=notificationSound).grid(row=5,column=1)

        pomodoroLength.set(str(self.pomodoroLength))
        shortBreakLength.set(str(self.shortBreakLength))
        longBreakLength.set(str(self.longBreakLength))
        pomodorosInGroup.set(str(self.pomodorosInGroup))
        autoplay.set("T" if self.autoplay else "F")
        notificationSound.set(self.notificationSound)

        ttk.Button(self.settingsMainframe, text='Cancel', command=close_window).grid(row=6,column=0)
        ttk.Button(self.settingsMainframe, text='Save Setings', command=save_settings).grid(row=6,column=1)

    def start_timer(self):
        self.startstopButton.configure(text='Pause Timer', command=self.pause_timer)
        self.timerOn = True
        self.startTime = t.time()
        if self.initialStartTime == 0:
            self.initialStartTime = self.startTime
        self.mainframe.after(0,self.timer)

    def pause_timer(self):
        self.startstopButton.configure(text='Resume Timer', command=self.start_timer)
        self.timerOn = False
        self.timeRan += t.time() - self.startTime
        self.timerSec -= t.time() - self.startTime

    def skip_timer(self):
        if self.timerOn: self.timeRan += t.time() - self.startTime
        self.timerOn = False
        if self.timerState == 'POMODORO': self.pomodoroCount += 1
        if self.timerState == 'POMODORO' and self.pomodoroCount%self.pomodorosInGroup != 0:
            self.timerState = 'SHORT BREAK'
            self.timerSec = self.shortBreakLength*60
            self.s.configure('TimerFrame.TFrame', background='spring green')
            self.s.configure('TimerFrame.TLabel', background='spring green')
            self.s.configure('TimerFrame.TButton', background='spring green')
            self.s.map('TimerFrame.TButton',background=[('active', 'pale green'),('pressed', 'pale green')])
        elif self.timerState == 'POMODORO' and self.pomodoroCount%self.pomodorosInGroup == 0:
            self.timerState = 'LONG BREAK'
            self.timerSec = self.longBreakLength*60
            self.s.configure('TimerFrame.TFrame', background='spring green')
            self.s.configure('TimerFrame.TLabel', background='spring green')
            self.s.configure('TimerFrame.TButton', background='spring green')
            self.s.map('TimerFrame.TButton',background=[('active', 'pale green'),('pressed', 'pale green')])
        elif self.timerState == 'SHORT BREAK' or self.timerState == 'LONG BREAK':
            self.timerState = 'POMODORO'
            self.timerSec = self.pomodoroLength*60
            self.s.configure('TimerFrame.TFrame', background='tomato')
            self.s.configure('TimerFrame.TLabel', background='tomato')
            self.s.configure('TimerFrame.TButton', background='tomato')
            self.s.map('TimerFrame.TButton',background=[('active', 'light coral'),('pressed', 'coral')])

        self.timerLabelVar.set("{}:00".format(int(self.timerSec/60)))
        self.pomodoroCountLabelVar.set("{}({})".format(int(self.pomodoroCount/self.pomodorosInGroup) + 1, self.pomodoroCount%self.pomodorosInGroup + 1))
        self.focusLabelVar.set("{}% Focus".format(round(100*(self.timeRan)/(t.time() - self.initialStartTime), 1)))
        self.startstopButton.configure(text='Start Timer', command=self.start_timer)

        if self.autoplay: self.start_timer()

    def timer(self):
        if self.timerOn:
            minutes = int(float(self.timerSec)/60 - (t.time()-self.startTime)/60)
            seconds = int(float(self.timerSec) - (t.time()-self.startTime))%60
            if seconds > 9:
                self.timerLabelVar.set("{}:{}".format(minutes, seconds))
            else:
                self.timerLabelVar.set("{}:0{}".format(minutes, seconds))

            self.focusLabelVar.set("{}% Focus".format(round(100*(self.timeRan + t.time() - self.startTime)/(t.time() - self.initialStartTime), 1)))

            if minutes < 1 and seconds < 1:
                self.skip_timer()
            else:
                self.mainframe.after(200,self.timer)

    def play_sound(self):

        pass

if __name__ == "__main__":
    root = Tk()
    pomodoro(root)
    root.mainloop()
