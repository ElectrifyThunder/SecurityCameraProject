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

class MainRoot():
    def __init__(self, cameraNumber, cameraLocation, cameraStatus,cameraFeed,Needs,cameraAmount,openedWindow):
        self.cameraNumber = cameraNumber
        self.cameraLocation = cameraLocation
        self.cameraStatus = cameraStatus
        self.cameraFeed = cameraFeed
        self.Needs = Needs
        self.cameraAmount = cameraAmount

    getNames = [ #Valid prisoner names here.
        "None", #This doesn't count it.
        "Doe",
        "Jane",
        "Dave",
        "Kevin",
        "John"
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
    def newtkinterWindow(self,windowName,loadButtons,addPrisoner):
        root = tk.Tk()
        root.title(windowName)
        root.geometry("800x600")  # Set the size of the root window
        MainRoot.setOpenedWindow(MainRoot,root)
        return root
    
    def setupNewPrisoner(prisonerName):
        prisonerName.append(prisonerName)

class loginRoot():
    #Get the login cridentials

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

MainRoot.setCameraFeed(MainRoot,[])
loginRoot.setNewAccount(loginRoot,False)
MainRoot.setCameraNumber(MainRoot,1)

#Functions

def focusedLostText(event):
    #textbox focused out
    text = event.widget
    labelName = event.widget._name
    if text.get() == "" and labelName == "password":
        PassText.insert(0,"Password")
        PassText.config(foreground="white")
    elif text.get() == "" and labelName == "username":
        UserText.insert(0,"Username")
        UserText.config(foreground="white")

def focusInText(event):
    #textbox focused in
    typeOfLabel = event.widget.get()
    labelName = event.widget._name

    if labelName == "password":
        PassText.delete(0,tk.END)
        PassText.config(foreground="white")
    elif labelName == "username":
        UserText.delete(0,tk.END)
        UserText.config(foreground="white")

def updateDropDown(cameraNumber,prisonerLabel,mainframe):
    #Dropdown list picker

    theRoot = MainRoot.getOpenedWindow(MainRoot)
    realNumber = int(cameraNumber)

    if len(str(realNumber)) <= 1:
        MainRoot.setCameraNumber(MainRoot,int(realNumber))
        try: 
            findPrisoner = MainRoot.getNames[realNumber]
            prisonerLabel.config(text=f"Prisoner Name: {findPrisoner}")
            MainRoot.setCameraNumber(MainRoot,cameraNumber)
            loadCamera(mainframe,f"Prisoner Room {realNumber}.jpg")
        except IndexError:
            prisonerLabel.config(text=f"Prisoner Not Found.")
 
            
imageLabels = []

def loadCamera(cameraRoot,room):
    #Loads the camera image here
    try:
        if imageLabels:
            for lbl in imageLabels:
                lbl.destroy()
            imageLabels.clear()

        # Remove the white background
        theImage = Image.open(room)
        # Resize the image
        resizedImage = theImage.resize((200, 200))
        tkImage3 = ImageTk.PhotoImage(resizedImage)

        imageLabel = Label(cameraRoot, image=tkImage3)
        imageLabel.pack()
        imageLabel.image = tkImage3
        imageLabels.append(imageLabel)

        MainRoot.setCameraFeed(cameraRoot,imageLabels)

    except FileNotFoundError:
        messagebox.showerror("Camera Not Found","Camera has Failed / Disconnected.")
        time.sleep(.5)
        if cameraRoot.winfo_exists():
            cameraRoot.destroy()

def handleButtonClick(prisonerNumber:Label, prisonerLabel:Label,camFrame:Frame,mainframe:Frame):
    frame_name = camFrame.winfo_name()
    prisonerNumber.config(text=f"Security Camera {frame_name}")

    # Safeguard against invalid inputs
    try:
        updateDropDown(frame_name,prisonerLabel,mainframe)
    except Exception as e:
        print(f"Error occurred: {e}")


def getTransparentImage(image):
    imageConvert = image.convert("RGBA")
    # Remove the white background
    data = imageConvert.getdata()
    new_data = []

    for item in data:
        # Replace white or near-white (RGB > 240) with transparent
        if item[0] > 240 and item[1] > 240 and item[2] > 240:
            new_data.append((255, 255, 255, 0))  # Transparent
        else:
            new_data.append(item)

    theImage.putdata(new_data)

    # Resize the image
    resizedImage = theImage.resize((200, 200))
    tkImage3 = ImageTk.PhotoImage(resizedImage)
    return tkImage3

def varSelect(selected_option, prisonerSpecs: OptionMenu):
    menu = prisonerSpecs["menu"]

    for index in range(menu.index("end") + 1):
        if menu.entrycget(index, "label") == selected_option:
            print(f"Selected option: {selected_option}, Index: {index}")
            menu.delete(index)
            break

def closeWindow():
    getTerminal = MainRoot.getOpenedWindow(MainRoot)
    getTerminal.destroy()

def loadMainProgram():
    #Main Program Loop Here
    cameraRoot = MainRoot.getOpenedWindow(MainRoot)
    
    #Content outerFrame
    outerGreenFrame = Frame(cameraRoot, bg="green", width=1200, height=600)  # Specify smaller dimensions
    outerGreenFrame.pack_propagate(False)  # Prevent resizing based on child widgets
    outerGreenFrame.place(relx=0.5, rely=0.5, anchor="center")  # Center it in the root

    contentCamera = Frame(outerGreenFrame,bg="Black")  # Match the content's background to root
    contentCamera.pack(expand=True, fill="both", padx=6, pady=6)  # Add padding inside for the border effect

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
    CloseButton = Button(cameraRoot,text="X", bg=mainFrame["bg"] ,fg="red", command=closeWindow)
    CloseButton.pack(side="left",fill="x")

    CloseButton.grid_rowconfigure(0,weight=1)
    CloseButton.grid_columnconfigure(0,weight=1)

    CloseButton.grid(row=0,column=0)

    #Handle all of the cameras added to the system.
    for i in range(4):
        # Open the image dynamically for each frame
        newImage = Image.open(f"Prisoner Room {i + 1}.jpg")  # Ensure filenames match your images
        
        # Resize the image
        resizedImage = newImage.resize((200, 200))  # Adjust the size as needed
        updatedImage = ImageTk.PhotoImage(resizedImage)
        
        # Add the frame
        newFrame = Frame(rowFrame, bg="grey", width=250, height=250, name=f"{i + 1}")
        newFrame.pack(side="left", padx=5)

        # Go to Camera Button
        goToCamera = Button(
            newFrame,
            text="Show Prisoner",
            bg=mainFrame["bg"],
            font=("Terminator", 12),
            fg="White",
            command=lambda frame=newFrame: handleButtonClick(cameraNumber, prisonerName,frame,mainFrame)
        )

        goToCamera.pack(expand=True)

        # Create a label with text and the image
        selectedName = Label(newFrame, text=f"Prisoner Name: {MainRoot.getNames[i + 1]}", image=updatedImage, compound="top", bg=mainFrame["bg"], fg="white", font=("Terminator", 12))
        selectedName.image = updatedImage
        selectedName.pack(expand=True)

    loadCamera(mainFrame,"Prisoner Room 1.jpg")

accountsFileName = "savedAccounts.txt"

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
                MainRoot.newtkinterWindow(MainRoot,"SecurityCameras",False,False)
                loadMainProgram()
            else:
                messagebox.showerror("Incorrect Account!", "Username or Password is incorrect!")

        except FileNotFoundError:
             messagebox.showerror("No file found.","save data file not found!")
        
#Main LoginScreen!
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
UserText.bind("<FocusIn>",focusInText)
UserText.bind("<FocusOut>",focusedLostText)
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
PassText.bind("<FocusIn>",focusInText)
PassText.bind("<FocusOut>",focusedLostText)
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

def checkbox_changed():
    if checkbox_var.get() == 1:
        checkBox.config(text="✅New Account")
        loginRoot.setNewAccount(loginRoot,True)
    else:
        checkBox.config(text="❌New Account")
        loginRoot.setNewAccount(loginRoot,False)

checkbox_var = tk.IntVar()
checkBox = Checkbutton(
    loginFrame,
    text="❌New Account",
    variable=checkbox_var,
    font="Terminator",
    command=checkbox_changed,
    indicatoron=False,  # Hides the checkbox, making it appear as a button
    bg="Lightgray",  # Background color for visibility
    fg="black",  # Text (foreground) color
    activebackground="darkgray",  # Background color when clicked
    activeforeground="white",  # Text color when clicked
    relief="raised",  # Adds a raised border to mimic a button
    bd=2  # Border width to make it pop
)
checkBox.pack()

# Create the root window
root.geometry("800x600")  # Set the size of the root window
root.mainloop()