from tkinter import *
from tkinter import colorchooser

# ----------------------------------------------------------------------
# my mainroot part
mainRoot=Tk()
mainRoot.iconbitmap('icons\\mainRoot.ico')
mainRoot.title('controlling system')

# ---------------------------------------------------
# size of main root
w=500
h=500
sw=mainRoot.winfo_screenwidth()
sh=mainRoot.winfo_screenheight()
x=(sw/2)-(w/2)
y=(sh/2)-(h/2)
mainRoot.geometry("%dx%d+%d+%d"%(w,h,x,y))
mainRoot.resizable(width=False, height=False)
# ---------------------------------------------------
# ---------------------------------------------------
# mySecurityPart

nameLabel=Label(master=mainRoot, text="Name:")
nameLabel.pack()

nameEntry=Entry(master=mainRoot)
nameEntry.pack()

passLabel=Label(master=mainRoot, text="Password:")
passLabel.pack()

passEntry=Entry(master=mainRoot)
passEntry.pack()

# control part
# -------------------------------
def control(event):
    pass



checkButton=Button(master=mainRoot, text="sign in", bg="#FFF5EE")
checkButton.bind("<Enter>", lambda event: checkButton.config(bg="#F3E5AB"))
checkButton.bind("<Leave>", lambda event: checkButton.config(bg="#FFF5EE"))
checkButton.bind("<Button>", control)
checkButton.pack()

# -------------------------------
# -------------------------------
# setting part
def setting(event):
    def changeColor(event):
        colorCode=colorchooser.askcolor(title="choose color")
        mainRoot.config(bg=colorCode[1])
    def selectMouseSensivity(event):
        pass
    
    def selectVolumeSensivity(event):
        pass
    # setRoot 
    setRoot=Tk()
    setRoot.title("setting")
    setRoot.iconbitmap("icons\\setting.ico")
    
    w=250
    h=250
    setRoot.geometry("%dx%d+%d+%d"%(w,h,200,200))
    setRoot.resizable(width=False, height=False)
    
    changeColorButton=Button(master=setRoot, text="change background color", bg="#FFF5EE")
    changeColorButton.bind("<Enter>", lambda event: changeColorButton.config(bg="#F3E5AB"))
    changeColorButton.bind("<Leave>", lambda event: changeColorButton.config(bg="#FFF5EE"))
    changeColorButton.bind("<Button>", changeColor)
    changeColorButton.pack()
    
    mouseSensitivityButton=Button(master=setRoot, text="set mouse sensitivity", bg="#FFF5EE")
    mouseSensitivityButton.bind("<Enter>", lambda event: mouseSensitivityButton.config(bg="#F3E5AB"))
    mouseSensitivityButton.bind("<Leave>", lambda event: mouseSensitivityButton.config(bg="#FFF5EE"))
    mouseSensitivityButton.bind("<Button>", selectMouseSensivity)
    mouseSensitivityButton.pack()
    
    volumeSensivityButton=Button(master=setRoot, text="set volume sensitivity", bg="#FFF5EE")
    volumeSensivityButton.bind("<Enter>", lambda event: volumeSensivityButton.config(bg="#F3E5AB"))
    volumeSensivityButton.bind("<Leave>", lambda event: volumeSensivityButton.config(bg="#FFF5EE"))
    volumeSensivityButton.bind("<Button>", selectVolumeSensivity)
    volumeSensivityButton.pack()
    
    
    setRoot.mainloop()


# set button
setButton=Button(master=mainRoot, text="setting", bg="#FFF5EE")
setButton.bind("<Enter>", lambda event: setButton.config(bg="#F3E5AB"))
setButton.bind("<Leave>", lambda event: setButton.config(bg="#FFF5EE"))
setButton.bind("<Button>", setting)
setButton.pack()
# -------------------------------


# exit button
exitButton=Button(master=mainRoot, text="Exit", bg="#FFF5EE")
exitButton.bind("<Enter>", lambda event: exitButton.config(bg="#F3E5AB"))
exitButton.bind("<Leave>", lambda event: exitButton.config(bg="#FFF5EE"))
exitButton.bind("<Button>", lambda event: mainRoot.destroy())
exitButton.pack()

# ---------------------------------------------------
# ---------------------------------------------------
# copyright frame
copyFrame=Frame(master=mainRoot, bg="#778899", width=500, height=15)
copyFrame.pack(side="bottom")
copyFrame.pack_propagate(0)

# copyright label
copyLabel=Label(master=copyFrame, text="@copyright-YasharZavaryRezaie-2023", bg="#778899")
copyLabel.pack(side="right")
# ---------------------------------------------------
# ---------------------------------------------------
# sign up part
def signUp(event):
    pass

# signup frame
signUpFrame=Frame(master=mainRoot, width=500, height=30)
signUpFrame.pack(side='bottom')
signUpFrame.pack_propagate(0)

signUpLabel=Label(master=signUpFrame, text="don't have a account?")
signUpLabel.pack(side="left")

signupButton=Button(master=signUpFrame, text="sign up", bg="#FFF5EE")
signupButton.bind("<Enter>", lambda event: signupButton.config(bg="#F3E5AB"))
signupButton.bind("<Leave>", lambda event: signupButton.config(bg="#FFF5EE"))
signupButton.bind("<Button>", signUp)
signupButton.pack(side="left")

# ---------------------------------------------------
# my mouse move function
def mouseProcess(event):
    pass

mouseMoveButton=Button(master=mainRoot, text="mouse mode", bg="#FFF5EE", fg="black")
mouseMoveButton.bind("<Enter>", lambda event: mouseMoveButton.config(bg="#F3E5AB"))
mouseMoveButton.bind("<Leave>", lambda event: mouseMoveButton.config(bg="#FFF5EE"))
mouseMoveButton.bind("<Button>", mouseProcess)
# mouseMoveButton.pack()
# ----------------------------------------------------


mainRoot.mainloop()
