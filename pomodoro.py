from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Pomodoro Timer")

mainframe = ttk.Frame(root, padding=(3, 10), borderwidth=2, relief='sunken')

label = ttk.Label(mainframe, text="This is a fancy program!")

button = ttk.Button(mainframe, text='Okay', command=lambda e:print("e"))

measureSystem = StringVar()
check = ttk.Checkbutton(mainframe, text='Use Metric', variable=measureSystem, onvalue='metric', offvalue='imperial')

username = StringVar()
entry = ttk.Entry(mainframe, textvariable=username)
username.trace_add("write", lambda e: print("Something was written"))

comboboxVar = StringVar()
combobox = ttk.Combobox(mainframe, textvariable=comboboxVar)

spinval = StringVar()
s = ttk.Spinbox(mainframe, from_=1.0, to=100.0, textvariable=spinval)

mainframe.grid(row=0,column=0, sticky=(N, S, E, W))
label.grid(row=0,column=0,columnspan=2)
button.grid(row=1,column=0)
check.grid(row=1,column=1)
entry.grid(row=2,column=0)
combobox.grid(row=3,column=0)
s.grid(row=4,column=0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(0,weight=1)
mainframe.columnconfigure(1,weight=1)
mainframe.rowconfigure(0,weight=1)
mainframe.rowconfigure(1,weight=1)
mainframe.rowconfigure(2,weight=1)
mainframe.rowconfigure(3,weight=1)
mainframe.rowconfigure(4,weight=1)


root.mainloop()
