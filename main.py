from tkinter import *


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
# mySecurityPart

nameLabel=Label(master=mainRoot, text="Name:")
nameLabel.pack()

nameEntry=Entry(master=mainRoot)
nameEntry.pack()

passLabel=Label(master=mainRoot, text="Password:")
passLabel.pack()

passEntry=Entry(master=mainRoot)
passEntry.pack()


# ---------------------------------------------------
# copyright frame
copyFrame=Frame(master=mainRoot, bg="#778899", width=500, height=15)
copyFrame.pack(side="bottom")
copyFrame.pack_propagate(0)

# copyright label
copyLabel=Label(master=copyFrame, text="@copyright-yasharZavaryRezaie-2023", bg="#778899")
copyLabel.pack(side="right")
# ---------------------------------------------------

# ---------------------------------------------------
# my mouse move function
def mouseProcess(event):
    pass

mouseMoveButton=Button(master=mainRoot, text="mouse mode", bg="#FFF5EE", fg="black")
mouseMoveButton.bind("<Enter>", lambda event: mouseMoveButton.config(bg="#F3E5AB"))
mouseMoveButton.bind("<Leave>", lambda event: mouseMoveButton.config(bg="#FFF5EE"))
mouseMoveButton.bind("<Button>", mouseProcess)
mouseMoveButton.pack()
# ----------------------------------------------------


mainRoot.mainloop()
