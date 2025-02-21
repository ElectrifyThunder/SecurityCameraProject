#Kobe Sensow
#2/21/2025
#Security Camera Interface for the sherif's department
#This program cycles through a simulation of 6 cameras viewing the prisoners
#It'll error out if it cannot find a linked camera in the data base.

#Services are here.
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import time
import random
from tkinter import messagebox
import math
import re

defaultLabel = "Enter camera number" #Default placeholder text

#Functions
def generateCameras():
    amountOfCameras = 6
    options = []
    for i in range(1, amountOfCameras):
        options.append(f"Security Camera {i}")
    return options

SecurityCameras = generateCameras() # We get the cameras and reload them here

root = tk.Tk()
root.title("Security Camera")

#Generated labels here
selectedOption = tk.StringVar()
selectedCamera = ttk.Label(root,text="")
cameraSelect = ttk.Combobox(root,textvariable=selectedOption,values=SecurityCameras,state="readonly")
cameraAlert = ttk.Label(root,text="Prisoner Needs:",anchor="w",justify="left")
frame = ttk.Frame(root,padding=10)
prisonerNeeds = ttk.Frame(root,padding=20)
text_var = tk.StringVar()
textBox = ttk.Entry(frame,foreground="grey")
cameraSelect.pack(padx=10,pady=10)
image2 = Image.open("clean prisoner.jpg")
image = Image.open("prison room.jpg")

selectedCamera.pack()

cameraAlert.pack(fill="x")
prisonerNeeds.pack(side="left", fill="both", expand=True)
frame.pack(fill="both",expand=True)

prisoners = []
extraItems = []
newWindow = None

#All of the functions here V

def on_entry_click(Entry): #When entered on the textbox
    textBox.delete(0,tk.END)
    textBox.config(foreground="black")

def on_entry_leave(Entry): #Reset to the default
    textBox.insert(0,defaultLabel)
    textBox.config(foreground="grey")

def test(event):
    button = event.widget  # Get the button that triggered the event
    button.destroy() 
    prisoners.remove(button)
    amountLeft = len(prisoners)

def buttonPrisoners(event): #Buttons saying what the prisoner wants
    global newWindow
    if newWindow:
        if newWindow is None or not newWindow.winfo_exists():
            newWindow = None
        return

    button = event.widget  # Get the button that triggered the event
    button.destroy() 
    prisoners.remove(button)
    amountLeft = len(prisoners)

    #Generate a new window item here
    if (amountLeft == 1) and (newWindow is None or not newWindow.winfo_exists()):
        newWindow = tk.Toplevel(root)
        newWindow.title("Extra Steps")
        newWindow.geometry("200x200")

        for i in range(1, 3):
                extraBtn = ttk.Button(newWindow, text="MedicineItem")
                extraBtn.bind("<Button-1>", test)
                extraBtn.pack()
                prisoners.append(extraBtn)
                
    if amountLeft == 0:
        selectedCamera.config(text="HAPPY PRISONER!")

def setPrisonerNeeds(): #This generates the basic needs for the buttons
    global prisoners
    for btn in prisoners:
        btn.pack_forget()
        btn.destroy()
    prisoners = []

    for i in range(1,random.randint(2,5)):
        button = ttk.Button(prisonerNeeds,text=f"prisoner needs: {random.randint(1,5)}")
        prisoners.append(button)
        button.pack()
        
        button.bind("<Button-1>", buttonPrisoners) #Assist their need

textBox.grid(row=0, column=0, padx=5, pady=5)
textBox.insert(0,defaultLabel)
textBox.pack()

prisonRoom = ImageTk.PhotoImage(image.resize((500,500)))
cleanPrisonRoom = ImageTk.PhotoImage(image2.resize((500,500)))

image_labels = []

def onOptionSelect(event):
    randomRoom = random.randint(1,2)

    global image_labels 
    
    for label in image_labels: #Delete any other camera copies here
        label.pack_forget()
        label.destroy()
    
    image_labels = []
    prisoners = []

    clickedOption = selectedOption.get()
    selectedCamera.config(text=clickedOption)
    
    currentImage = None

    if randomRoom == 2:
        currentImage = tk.Label(root,image=prisonRoom) #Create a new camera copy
        currentImage.pack(pady=20)
    else:  
        currentImage = tk.Label(root,image=cleanPrisonRoom) #Create a new camera copy
        currentImage.pack(pady=20)

    image_labels.append(currentImage)

    setPrisonerNeeds() #Set prisoner needs!

def showWhatWrittened(event):
    text = textBox.get()
    if text.isdigit() and len(text) == 1: # we check if its a digit

        camera = int(text) - 1

        try: # We try to find a available camera 
            cameraSelect.current(camera)
            onOptionSelect(event)
        except (ValueError,tk.TclError) as e:
            messagebox.showerror("No Camera Found",f"Camera {text} Does not exist!")
        textBox.delete(0,tk.END)
        root.focus_set()
    else:
        if len(text) == 1:
            messagebox.showerror("Must be a number","Input must be a number!")
        else:
            messagebox.showerror("Input must be 1 character","Input is too long!")
        
        textBox.delete(0,tk.END)
        textBox.config(foreground="grey")
        root.focus_set()

#All of the events held here.
textBox.bind('<FocusIn>',on_entry_click)
textBox.bind("<FocusOut>",on_entry_leave)
textBox.bind("<Return>", showWhatWrittened)
cameraSelect.bind("<<ComboboxSelected>>",onOptionSelect)
cameraSelect.current(0)

root.mainloop()

