from tkinter import *
from tkinter import ttk
import os as os
import subprocess as sp
import random as random
import time as t

soundNames = []

def get_sound_names():
    for file in os.listdir("sounds"):
        if file.endswith(".mp3") or file.endswith(".wav"):
            soundNames.append(file)

def play_sound(fileName):
    basePath = os.getcwd()
    sp.Popen(['afplay', '{}/sounds/{}'.format(basePath, fileName)])

class pomodoro:
    def __init__(self, parent):
        # Initializing Variables
        self.pomodoroLength = 25
        self.shortBreakLength = 5
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
        self.notificationSound = soundNames[0]

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
        self.s.configure('TaskFrame.TLabel', background='grey')

        self.s.configure('Task.TaskFrame.TLabel', background='grey')
        self.s.configure('Task.TaskFrame.TCheckbutton', background='grey')
        self.s.configure('Task.TaskFrame.TEntry', background='grey', fieldbackground='grey', borderwidth=0)
        self.s.configure('Task.TaskFrame.TMenubutton', background='grey')

        # Creating mainframe
        self.mainframe = ttk.Frame(parent)
        self.mainframe.grid(row=0,column=0,sticky="N E S W")

        # Creating and placing containers
        self.timerFrame = ttk.Frame(self.mainframe, style='TimerFrame.TFrame')
        self.taskFrame = ttk.Frame(self.mainframe, style='TaskFrame.TFrame')
        self.doneFrame = ttk.Frame(self.mainframe, style='doneFrame.TFrame')

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

        # Creating and placing taskFrame widgets
        self.taskEntryVar = StringVar()
        self.taskLabelVar = StringVar(); self.taskLabelVar.set("Tasks: 0")

        self.taskLabel = ttk.Label(self.taskFrame, textvariable=self.taskLabelVar, style='TaskFrame.TLabel')
        self.taskEntry = ttk.Entry(self.taskFrame, textvariable=self.taskEntryVar, style='TaskFrame.TEntry')
        self.addTaskButton = ttk.Button(self.taskFrame, text='+', command=self.add_task, style='TaskFrame.TButton')
        #self.scheduleButton = ttk.Button(self.taskFrame, text='Schedule', command=self.open_schedule, style='TaskFrame.TButton')

        self.taskCount = 0
        self.taskList = []
        self.taskListFrame = ttk.Frame(self.taskFrame, style='TaskFrame.TFrame')

        self.taskLabel.grid(row=0,column=0,columnspan=2,sticky='EW')
        self.taskEntry.grid(row=1,column=0,sticky='EW',ipady=5)
        self.addTaskButton.grid(row=1,column=1,sticky='EW')
        #self.scheduleButton.grid(row=1,column=2,sticky='EW')
        self.taskListFrame.grid(row=2,column=0,columnspan=2,sticky='NESW')

        # Creating and placing doneFrame widgets
        self.doneLabelVar = StringVar(); self.doneLabelVar.set('Complete : 0')

        self.doneLabel = ttk.Label(self.doneFrame, textvariable=self.doneLabelVar, style='DoneFrame.TLabel')
        self.doneListFrame= ttk.Frame(self.doneFrame, style='DoneFrame.TFrame')
        self.doneListFrame.grid(row=0,column=0,sticky='NESW')
        self.doneCount= 0
        self.doneList = []

        # row/column configure
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)

        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1,minsize=100)
        self.mainframe.rowconfigure(1, weight=2,minsize=200)
        self.mainframe.rowconfigure(2, weight=2,minsize=200)

        self.timerFrame.columnconfigure(0, weight=1,minsize=100)
        self.timerFrame.columnconfigure(1, weight=5,minsize=100)
        self.timerFrame.columnconfigure(2, weight=5,minsize=100)
        self.timerFrame.columnconfigure(3, weight=1,minsize=100)
        self.timerFrame.rowconfigure(0, weight=1)
        self.timerFrame.rowconfigure(1, weight=5)
        self.timerFrame.rowconfigure(2, weight=5)
        self.timerFrame.rowconfigure(3, weight=1)

        self.taskFrame.columnconfigure(0,weight=1,minsize=200)
        self.taskFrame.columnconfigure(1,weight=0,minsize=50)
        #self.taskFrame.columnconfigure(2,weight=0,minsize=50)
        self.taskFrame.rowconfigure(0,weight=0,minsize=10)
        self.taskFrame.rowconfigure(1,weight=0,minsize=10)
        #self.taskFrame.rowconfigure(2,weight=1,minsize=200)
        self.taskListFrame.columnconfigure(0,weight=1,minsize=200)

        self.doneFrame.columnconfigure(0,weight=1)
        self.doneFrame.rowconfigure(0,weight=1)
        self.doneListFrame.columnconfigure(0,weight=1,minsize=200)


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
        self.s.configure('TimerFrame.TFrame', background='tomato')
        self.s.configure('TimerFrame.TLabel', background='tomato')
        self.s.configure('TimerFrame.TButton', background='tomato')
        self.s.map('TimerFrame.TButton',background=[('active', 'light coral'),('pressed', 'coral')])

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
        ttk.Combobox(self.settingsMainframe, values=soundNames, state='readonly', textvariable=notificationSound).grid(row=5,column=1)

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

        if self.timerState == 'POMODORO':
            self.pomodoroCount += 1
            for task in self.taskList:
                if task['checkbox'].get() == 'T':
                    task['time'] += self.pomodoroLength
                    task['pomodoros'] += 1
                    task['time taken'].set('  ({}) {}h {}m  '.format(task['pomodoros'], int(task['time']/60), task['time']%60))


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

        play_sound(self.notificationSound)

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

    def add_task(self):
        self.taskList.append({})
        self.taskList[-1]['base frame'] = ttk.Frame(self.taskListFrame, style='Task.TaskFrame.TFrame') # frame
        self.taskList[-1]['checkbox'] = StringVar() # checkbox var
        self.taskList[-1]['name'] = StringVar(); self.taskList[-1]['name'].set(self.taskEntryVar.get()) # name entry var
        self.taskList[-1]['time'] = 0
        self.taskList[-1]['pomodoros'] = 0
        self.taskList[-1]['time taken'] = StringVar(); self.taskList[-1]['time taken'].set('  (0) 0h 0m  ') # Time taken label var
        self.taskList[-1]['time expected'] = StringVar(); self.taskList[-1]['time expected'].set('0m') # Time expected entry var

        self.taskList[-1]['base frame'].grid(row=self.taskCount,column=0,sticky='EW')

        ttk.Checkbutton(self.taskList[-1]['base frame'], variable=self.taskList[-1]['checkbox'], onvalue='T', offvalue='F', style='Task.TaskFrame.TCheckbutton').grid(row=0,column=0,sticky='EW')
        ttk.Entry(self.taskList[-1]['base frame'], textvariable=self.taskList[-1]['name'], style='Task.TaskFrame.TEntry').grid(row=0,column=1,sticky='EW')
        ttk.Label(self.taskList[-1]['base frame'], textvariable=self.taskList[-1]['time taken'], style='Task.TaskFrame.TLabel').grid(row=0,column=2,sticky='EW')
        ttk.Entry(self.taskList[-1]['base frame'], textvariable=self.taskList[-1]['time expected'], width = 6, style='Task.TaskFrame.TEntry').grid(row=0,column=3,sticky='EW')

        menubutton = ttk.Menubutton(self.taskList[-1]['base frame'], text='...', width=3, style='Task.TaskFrame.TMenubutton')
        menubutton.menu = Menu(menubutton)
        menubutton['menu'] = menubutton.menu
        self.taskList[-1]['menu'] = menubutton.menu
        menubutton.grid(row=0,column=4,sticky='EW')
        self.taskList[-1]['menu'].add_command(label='Delete Task', command=lambda i=self.taskCount: self.delete_task(i))
        self.taskList[-1]['menu'].add_command(label='Complete Task', command=lambda i=self.taskCount: self.complete_task(i))

        self.taskListFrame.rowconfigure(self.taskCount,weight=0)

        self.taskList[-1]['base frame'].columnconfigure(0,weight=0,minsize=10)
        self.taskList[-1]['base frame'].columnconfigure(1,weight=5,minsize=100)
        self.taskList[-1]['base frame'].columnconfigure(2,weight=0,minsize=25)
        self.taskList[-1]['base frame'].columnconfigure(3,weight=0,minsize=25)
        self.taskList[-1]['base frame'].columnconfigure(4,weight=0,minsize=10)

        self.taskCount += 1

        self.taskEntryVar.set('')
        self.taskLabelVar.set('Tasks: {}'.format(self.taskCount))

    def delete_task(self, index):
        self.taskList[index]['base frame'].grid_forget()
        del self.taskList[index]
        for i in range(index, len(self.taskList)):
            self.taskList[i]['base frame'].grid_forget()
            self.taskList[i]['base frame'].grid(row=i,column=0,sticky='EW')
            self.taskList[i]['menu'].entryconfig(0, command=lambda i=i: self.delete_task(i))
            self.taskList[i]['menu'].entryconfig(1, command=lambda i=i: self.complete_task(i))
        self.taskCount -= 1
        self.taskLabelVar.set('Tasks: {}'.format(self.taskCount))

    def complete_task(self, index):
        self.taskList[index]['base frame'].grid_forget()
        baseFrame = ttk.Frame(self.doneListFrame, style='Done.DoneListFrame.TFrame')
        self.doneList.append(baseFrame)
        self.doneList[-1].grid(row=self.doneCount, column=0,sticky='EW')

        ttk.Label(self.doneList[-1], text=self.taskList[index]['name'].get(), style='Task.DoneFrame.TLabel').grid(row=0,column=0,sticky='W')
        ttk.Label(self.doneList[-1], text=self.taskList[index]['time taken'].get(), style='Task.DoneFrame.TLabel').grid(row=0,column=1,sticky='E')

        self.doneListFrame.rowconfigure(self.doneCount,weight=0)

        self.doneList[-1].columnconfigure(0,weight=1,minsize=150)
        self.doneList[-1].columnconfigure(1,weight=0,minsize=50)

        self.doneCount+= 1

        self.doneLabelVar.set('Comeplete: {}'.format(self.taskCount))

    #def open_schedule(self):
    #    pass

if __name__ == "__main__":
    root = Tk()
    get_sound_names()
    if len(soundNames) == 0:
        print("Sounds file empty")
        exit()
    pomodoro(root)
    root.mainloop()
