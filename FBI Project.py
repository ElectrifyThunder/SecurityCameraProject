#Kobe Sensow
#2/21/2025
#Security Camera Interface for the sherif's department
#This program creates a login screen for the Agent F.B.I database to view available cameras

#Services are here.
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter.font import Font
from PIL import Image, ImageTk
import time
from tkinter import messagebox
import math
import re
from tkinter import Frame,Entry,Label,Checkbutton,Button,OptionMenu #Confirmed Labels I'll be using today.

accountsFileName = "savedAccounts.txt"

class MainRoot(): #MainRoot Window
    def __init__(self, cameraNumber, cameraLocation, cameraStatus,cameraFeed,Needs,cameraAmount,loadedFrames):
        self.cameraNumber = cameraNumber
        self.cameraLocation = cameraLocation
        self.cameraStatus = cameraStatus
        self.cameraFeed = cameraFeed
        self.Needs = Needs
        self.cameraAmount = cameraAmount
        self.loadedFrames = loadedFrames

    getNames = [ #Valid prisoner names here.
        "None", #This doesn't count it.
        "doe",
        "jane",
        "dave",
        "kevin",
        "john"
    ]

    #Getters
    def getCameraNumber(self):
        return self.cameraNumber
    def getCameraFeed(self):
        return self.cameraFeed
    def getAmountOfCameras(self):
        return self.cameraAmount
    def getOpenedWindow(self):
        return self.openedWindow
    
    #Active
    def setCameraNumber(self,cameraNumber):
        self.cameraNumber = cameraNumber
    def setCameraFeed(self,cameraFeed):
        self.cameraFeed = cameraFeed
    def setCameraAmount(self,cameraAmount):
        self.cameraAmount = cameraAmount
    def setOpenedWindow(self,openedWindow):
        self.openedWindow = openedWindow

       #Functions
    def newtkinterWindow(self,windowName):
        root = tk.Tk()
        root.title(windowName)
        root.geometry("800x600")
        MainRoot.setOpenedWindow(MainRoot,root)
        return root

class loginRoot():  #Get the login cridentials
    def __init__(self, newAccount, Password, Username):
        self.newAccount = newAccount
        self.Password = Password
        self.Username = Username
    
    def getNewAccount(self):
        return self.newAccount
    def getUserPassword(self):
        return self.Password
    def getUserUsername(self):
        return self.Username
    
    def setNewAccount(self,newAccount):
        self.newAccount = newAccount
    def setUserPassword(self,Password):
        self.Password = Password
    def setUserUsername(self,Username):
        self.Username = Username

#We add the default attributes here..
loginRoot.setNewAccount(loginRoot,False)
MainRoot.setCameraNumber(MainRoot,1)
imageLabels = []

#Functions
def focusedLostText(event,untLabel): #Text gets focused out here
    text = event.widget
    labelName = event.widget._name
    newName = ""
    uniqueColor = ""

    if text.get() == "" and labelName == "password":
        newName = "Password"
        uniqueColor = "White"
    elif text.get() == "" and labelName == "username":
        newName = "Username"
        uniqueColor = "White"
    elif text.get() == "" and labelName == "prisonername":
        newName = "New Prisoner Name"
        uniqueColor = "black"
    else:
        uniqueColor = "White"
    
    untLabel.insert(0,newName)
    untLabel.config(foreground=uniqueColor)

def focusInText(event,untLabel): #Focused in text here
    labelName = event.widget._name
    uniqueColor = ""
    
    if labelName == "password":
        uniqueColor = "White"
    elif labelName == "username":
        uniqueColor = "White"
    elif labelName == "prisonername":
        uniqueColor = "black"
    else:
        uniqueColor = "White"

    untLabel.delete(0,tk.END)
    untLabel.config(foreground=uniqueColor)
    
def updateMainCamera(cameraNumber,prisonerLabel,mainframe): #Updates the top label of camera
    realNumber = int(cameraNumber)
    MainRoot.setCameraNumber(MainRoot,int(realNumber))
    try: 
        findPrisoner = MainRoot.getNames[realNumber]
        prisonerLabel.config(text=f"Prisoner Name: {findPrisoner}")
        MainRoot.setCameraNumber(MainRoot,cameraNumber)
        loadCamera(mainframe,f"Prisoner Room {realNumber}.jpg")
    except IndexError:
        prisonerLabel.config(text=f"Prisoner Not Found.")


def loadCamera(cameraRoot,room): #Tries to load the cameras here
    try:
        if imageLabels:
            for lbl in imageLabels:
                lbl.destroy()
            imageLabels.clear()
        
        theImage = Image.open(room)
        resizedImage = theImage.resize((200, 200))
        tkImage3 = ImageTk.PhotoImage(resizedImage)

        imageLabel = Label(cameraRoot, image=tkImage3)
        imageLabel.pack()
        imageLabel.image = tkImage3
        imageLabels.append(imageLabel)

        MainRoot.setCameraFeed(cameraRoot,imageLabels)

    except FileNotFoundError: #If no image file is found in the file.
        messagebox.showerror("Camera Not Found","Camera has Failed / Disconnected.")
        time.sleep(.5)
        if cameraRoot.winfo_exists():
            cameraRoot.destroy()

def handleButtonClick(prisonerNumber:Label, prisonerLabel:Label,camFrame:Frame,mainframe:Frame):
    frame_name = camFrame.winfo_name()
    prisonerNumber.config(text=f"Security Camera {frame_name}")
    updateMainCamera(frame_name,prisonerLabel,mainframe)

def getTransparentImage(image): #Makes a image transparent
    imageConvert = image.convert("RGBA")
    data = imageConvert.getdata()
    new_data = []

    for item in data:
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    theImage.putdata(new_data)

    resizedImage = theImage.resize((200, 200))
    tkImage3 = ImageTk.PhotoImage(resizedImage)
    return tkImage3

def closeWindow(): #Closes the window
    getTerminal = MainRoot.getOpenedWindow(MainRoot)
    getTerminal.destroy()

def checkbox_changed(event,checkVar,checkLabel): #Checks if checkbox has been changed.
    answer = checkVar.get()
    if answer == 1:
        checkLabel.config(text="✅New Account")
        loginRoot.setNewAccount(loginRoot,True)
    elif answer == 0:
        checkLabel.config(text="❌New Account")
        loginRoot.setNewAccount(loginRoot,False)
    else:
        messagebox.showerror("Error occured","This isn't suppose to happen.")
    
def changePrisonerName(changeTo:Entry, nameLabel:Label): #New Entry For Prisoner Name
    whatNeedsChanged = changeTo.get()
    theName = nameLabel.cget("text").replace("Prisoner Name:", "").strip()

    for index, name in enumerate(MainRoot.getNames):
        if name.lower() == theName.lower():
            MainRoot.getNames[index] = whatNeedsChanged
            nameLabel.config(text="Prisoner Name: "+whatNeedsChanged)
            changeTo.delete(0,tk.END)
            changeTo.insert(0,"New Prisoner Name")
            changeTo.config(foreground="grey")
            break

def loadMainProgram(): #Main program loop
    cameraRoot = MainRoot.getOpenedWindow(MainRoot)
    
    #Content outerFrame
    outerGreenFrame = Frame(cameraRoot, bg="green", width=1200, height=600)
    outerGreenFrame.pack_propagate(False)
    outerGreenFrame.place(relx=0.5, rely=0.5, anchor="center")

    contentCamera = Frame(outerGreenFrame,bg="Black")
    contentCamera.pack(expand=True, fill="both", padx=6, pady=6)

    #Main Body
    mainFrame = Frame(contentCamera,bg="black")
    mainFrame.pack(padx=5,pady=5)

    # Another begin here
    selectedOption = tk.StringVar(contentCamera)
    selectedOption.set("Security Number 1")

    cameraNumber = Label(mainFrame,text=f"Camera Number:{MainRoot.getCameraNumber(MainRoot)}",font=("Terminator",12),bg=mainFrame["bg"],fg="white")
    cameraNumber.pack()

    prisonerName = Label(mainFrame,text=f"Prisoner Name: {MainRoot.getNames[1]}",bg=mainFrame["bg"],font=("Terminator",12),fg="white")
    prisonerName.pack()

    rowFrame = Frame(contentCamera,bg="Black")
    rowFrame.pack(pady=10)

    #User labels
    topFrame = Frame(mainFrame)
    topFrame.pack(side="top", fill="x")

    topFrame.grid_rowconfigure(0, weight=1)
    topFrame.grid_columnconfigure(0, weight=1)

    accountName = Label(topFrame, text=f"Agent Username: {loginRoot.getUserUsername(loginRoot)}",font=("Terminator",12))
    accountName.grid(row=0, column=0)

    #Close Terminal
    CloseButton = Button(cameraRoot,text="X", bg=mainFrame["bg"] ,fg="red", font=("Terminator",20), command=closeWindow)
    CloseButton.pack(side="left",fill="x")

    CloseButton.grid_rowconfigure(0,weight=1)
    CloseButton.grid_columnconfigure(0,weight=1)

    CloseButton.grid(row=0,column=0)

    #Handle all of the cameras added to the system.
    AmountOfCameras = 4

    for i in range(AmountOfCameras): 
        newImage = Image.open(f"Prisoner Room {i + 1}.jpg")
        resizedImage = newImage.resize((200, 200))
        updatedImage = ImageTk.PhotoImage(resizedImage)

        newFrame = Frame(rowFrame, bg="grey", width=250, height=250, name=f"{i + 1}")
        newFrame.pack(side="left", padx=5)

        goToCamera = Button(
            newFrame,
            text="Show Prisoner",
            bg=mainFrame["bg"],
            font=("Terminator", 12),
            fg="White",
            command=lambda frame=newFrame: handleButtonClick(cameraNumber, prisonerName,frame,mainFrame)
        )
        goToCamera.pack(expand=True)

        unique_name = MainRoot.getNames[i + 1].lower()
        
        selectedName = Label(newFrame, text=f"Prisoner Name: {MainRoot.getNames[i + 1]}",image=updatedImage, compound="top", bg=mainFrame["bg"], fg="white", font=("Terminator", 12), name=f"{unique_name}")
        selectedName.image = updatedImage
        selectedName.pack(expand=True)

        changeName = Entry(newFrame,name="prisonername")
        changeName.insert(0,"New Prisoner Name")
        changeName.pack()

        #Call back functions here
        changeName.bind("<FocusIn>",lambda event, changeName=changeName:focusInText(event,changeName))
        changeName.bind("<FocusOut>",lambda event,changeName=changeName:focusedLostText(event,changeName))
        changeName.bind("<Return>", lambda event, changeName=changeName, name=unique_name, selectedName=selectedName: changePrisonerName(changeName,selectedName))

    #Load the default camera
    loadCamera(mainFrame,"Prisoner Room 1.jpg")

#Main Login
def loggingin():
    #Main labels:
    savedUser = UserText.get()
    savedPass = PassText.get()
    makingANewAccount = loginRoot.getNewAccount(loginRoot)

    #Create a new account here
    if makingANewAccount and savedPass!="" and savedUser !="" and savedPass !="Password" and savedUser !="Username":
        try:
            # Open the file in read mode to check existing entries
            with open(accountsFileName, "r") as file:
                existing_accounts = file.readlines()

            #Combined labels to search:
            labelUser = f"Username: {savedUser}"
            labelPass = f"Password: {savedPass}"

            # Check if the user and password already exist
            account_exists = any(labelUser in line and labelPass in line for line in existing_accounts)

            if not account_exists:
                # Open the file in append mode to add the new account
                with open(accountsFileName, "a") as file:
                    file.write(f"{labelUser} {labelPass}\n")
                messagebox.showinfo("Saved Successfully", f"Account: {savedUser} created!")
            else:
                messagebox.showerror("Exists already!", "Username or Password already exists!")
        except FileNotFoundError:
            messagebox.showerror("No file found.","save data file not found!")
        
    #The user submits it and loggs them in, possibly?
    if not makingANewAccount and savedPass != "" and savedUser != "" and savedPass != "Password" and savedUser != "Username":
        try:
            with open(accountsFileName, "r") as file:
                existing_accounts = file.readlines()

            # Combine username and password as the unique label
            labelUser = f"Username: {savedUser}"
            labelPass = f"Password: {savedPass}"

            # Check if the user and password already exist
            account_exists = any(labelUser in line and labelPass in line for line in existing_accounts)

            if account_exists:
                loginRoot.setUserPassword(loginRoot,savedPass)
                loginRoot.setUserUsername(loginRoot,savedUser)
                root.destroy()
                MainRoot.newtkinterWindow(MainRoot,"SecurityCameras")
                loadMainProgram()
            else:
                messagebox.showerror("Incorrect Account!", "Username or Password is incorrect!")
        except FileNotFoundError:
             messagebox.showerror("No file found.","save data file not found!")
        

#Main LoginScreen! - Start Here..
root = tk.Tk()

root.config(bg="Black")
root.title("F.B.I Terminal")

# Create the outer yellow frame (border)
outerYellowFrame = Frame(root, bg="yellow", width=1200, height=600)  # Specify smaller dimensions
outerYellowFrame.pack_propagate(False)  # Prevent resizing based on child widgets

# Use the place geometry manager to center the frame
outerYellowFrame.place(relx=0.5, rely=0.5, anchor="center")  # Center it in the root

# Create the content frame inside the yellow border
contentFrame = Frame(outerYellowFrame, bg=root["bg"])  # Match the content's background to root
contentFrame.pack(expand=True, fill="both", padx=3, pady=3)  # Add padding inside for the border effect

theImage = Image.open("FBI Logo.png")
FBILogo = getTransparentImage(theImage)

# Apply the transparent image
imageLabel = Label(
        contentFrame, 
        image=FBILogo, 
        bg=root["bg"]
        )  

# Match the label's background to root
imageLabel.image = FBILogo  # Keep a reference to prevent garbage collection
imageLabel.pack()

welcomeLabel = Label(
    contentFrame,text="F.B.I. T E R M I N A L",
    font=("Terminator",20),
    bg=root["bg"],
    fg="White",
)

welcomeLabel.pack(pady=10)

outerFrame = Frame(contentFrame,bg="red")
outerFrame.pack(padx=30,pady=30)

loginFrame = Frame(outerFrame,
                bg=root["bg"],
                )

loginFrame.pack(padx=2,pady=2)

UserLabel = Label(
    loginFrame,text="Enter Username: ",
    font="Terminator",
    bg=root["bg"],
    fg="White"
)

UserLabel.pack()

UserText = Entry(
    loginFrame,
    name="username",
    fg="white",  # Correct text color
    bg=root["bg"],  # Background color matches the root
    font="Terminator"
)

UserText.insert(0,"Username")
UserText.bind("<FocusIn>",lambda event, UserText = UserText: focusInText(event,UserText))
UserText.bind("<FocusOut>",lambda event, UserText=UserText: focusedLostText(event,UserText))
UserText.pack()

PassLabel = Label(loginFrame,bg=root["bg"],fg="White",font="Terminator",text="Enter Password:")
PassLabel.pack()

PassText = Entry(
    loginFrame,
    name="password",
    fg="white",  # Correct text color
    bg=root["bg"],  # Background color matches the root
    font="Terminator"
)

PassText.insert(0,"Password")
PassText.bind("<FocusIn>",lambda event, PassText=PassText: focusInText(event,PassText))
PassText.bind("<FocusOut>",lambda event, PassText=PassText: focusedLostText(event,PassText))
PassText.pack()

submitAccount = Button(contentFrame,text="Login", foreground="grey",bg=root["bg"],fg="White",font="Terminator", command=loggingin)
submitAccount.pack()

descriptionLabel = Label(
    contentFrame,
    text="This is a secured Federal government system.  Unauthorized access is stricitly prohibited. All actrivity is fully monitored. Individuals who attempt to gain unauthorized access to this system are subject to Federal criminal prosecution.",                
    bg=root["bg"],
    fg="White",
    font="Terminator",
    justify="left",
    wraplength=800,
)

descriptionLabel.pack()

checkbox_var = tk.IntVar(value=1)
checkBox = Checkbutton(
    loginFrame,
    text="❌New Account",
    variable=checkbox_var,
    font="Terminator",
    indicatoron=False,
    bg="Lightgray",
    fg="black",
    activebackground="darkgray",
    activeforeground="white",
    relief="raised",
    bd=2
)
checkBox.bind("<ButtonPress>",lambda event,checkBox=checkBox:checkbox_changed(event,checkbox_var,checkBox))
checkBox.pack()

# Create the root window
root.geometry("800x600")  # Set the size of the root window
root.mainloop()