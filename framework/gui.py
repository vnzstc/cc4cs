# GUI interface 
import tkinter as tk
from functools import partial

import os 

def returnDirNames(topDir):
	return [f for f in os.listdir(topDir) if os.path.isdir(os.path.join(topDir, f))]

def btnCallback(lbox, rbtn):
   print(lbox.get(tk.ACTIVE))
   print(rbtn.get())

# Main GUI window
root = tk.Tk()
root.title("CC4CS Calculator")
root.geometry("300x400")
root.resizable(0, 0)  # Don't allow resizing in the x or y direction

# First Frame Section - Listbox code
## Frame used for the listbox 
fFrame = tk.Frame(root, relief=tk.GROOVE, width=250, height=300, padx=10, pady=5)
fFrame.pack(fill=tk.X)

var = tk.StringVar()
label = tk.Label(fFrame, textvariable=var, relief=tk.RIDGE)
var.set("Benchmark Functions")
label.pack(pady=5, fill=tk.X)

## Creates the listbox
lbox = tk.Listbox(fFrame, height=16)
lbox.pack(fill=tk.X)

## Insert list names 
for item in returnDirNames('./benchmark'):
    lbox.insert(tk.END, item)

## Make the first element as the default selection
lbox.select_set(0)
lbox.event_generate("<<ListboxSelect>>")

# Second Frame Section - Checkbar code
micros = ['8051', 'Leon3', 'Atmega328p']

sFrame = tk.Frame(root, relief=tk.GROOVE, height=45, padx=10)
sFrame.pack(fill=tk.X)

var = tk.StringVar()
label = tk.Label(sFrame, textvariable=var, relief=tk.RIDGE)
var.set("Microprocessors")
label.pack(fill=tk.X)

var = tk.IntVar()
for idx, item in enumerate(micros):
	chk = tk.Radiobutton(sFrame, text=item, variable=var, value=idx)
	chk.pack(side=tk.LEFT,  fill=tk.X, expand=True)

# Third Frame Section - Button code
tFrame = tk.Frame(root, relief=tk.GROOVE, height=10, padx=10, pady=15)
tFrame.pack(fill=tk.X)

button = tk.Button(tFrame, text ="Calculate CC4CS", command=partial(btnCallback, lbox, var))
button.pack(fill=tk.X)

root.grid()
root.mainloop()