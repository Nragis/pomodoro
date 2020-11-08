from tkinter import *
from tkinter import ttk
import random as random
import time as t


class pomodoro(object):
    def __init__(self, parent):
        # Initializing Variables
        self.pomodoroLength = 25
        self.shortBreakLength = 1
        self.longBreakLength = 15
        self.pomodoroInGroup = 4
        self.pomodoroCount = 0
        self.timerMin = self.pomodoroLength

        self.timerOn = False
        self.timerState = 'POMODORO'

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

        # Creating and placing taskFrame widgets
        self.timerLabelVar = StringVar(); self.timerLabelVar.set('Timer')
        self.focusLabelVar = StringVar()
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
        pass

    def open_settings(self):
        pass

    def start_timer(self):
        self.startstopButton.configure(text='Pause Timer', command=self.pause_timer)
        self.timerOn = True
        self.startTime = t.time()
        self.mainframe.after(0,self.timer)

    def pause_timer(self):
        self.startstopButton.configure(text='Resume Timer', command=self.resume_timer)
        self.timerOn = False

    def resume_timer(self):
        self.startstopButton.configure(text='Pause Timer', command=self.pause_timer)
        self.timerOn = True
        self.mainframe.after(0,self.timer)

    def skip_timer(self):
        self.timerOn = False
        if self.timerState == 'POMODORO': self.pomodoroCount += 1
        if self.timerState == 'POMODORO' and self.pomodoroCount%self.pomodoroInGroup != 0:
            self.timerState = 'SHORT BREAK'
            self.timerMin = self.shortBreakLength
        elif self.timerState == 'POMODORO' and self.pomodoroCount%self.pomodoroInGroup == 0:
            self.timerState = 'LONG BREAK'
            self.timerMin = self.longBreakLength
        elif self.timerState == 'SHORT BREAK' or self.timerState == 'LONG BREAK':
            self.timerState = 'POMODORO'
            self.timerMin = self.pomodoroLength

        self.timerLabelVar.set("{}:00".format(self.timerMin))
        self.pomodoroCountLabelVar.set("{}({})".format(int(self.pomodoroCount/self.pomodoroInGroup) + 1, self.pomodoroCount%self.pomodoroInGroup + 1))

        self.startstopButton.configure(text='Start Timer', command=self.start_timer)


    def timer(self):
        if self.timerOn:
            minutes = int(float(self.timerMin) - (t.time()-self.startTime)/60)
            seconds = int(float(self.timerMin)*60 - (t.time()-self.startTime))%60
            if seconds > 9:
                self.timerLabelVar.set("{}:{}".format(minutes, seconds))
            else:
                self.timerLabelVar.set("{}:0{}".format(minutes, seconds))

            if minutes < 1 and seconds < 1:
                self.skip_timer()
            else:
                self.mainframe.after(200,self.timer)



if __name__ == "__main__":
    root = Tk()
    pomodoro(root)
    root.mainloop()
