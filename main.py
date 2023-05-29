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

# ---------------------------------------------------
# copyright frame
copyFrame=Frame(master=mainRoot, bg="#778899", width=500, height=15)
copyFrame.pack(side="bottom")
copyFrame.pack_propagate(0)

# copyright label
copyLabel=Label(master=copyFrame, text="@copyright-yasharZavaryRezaie-2023", bg="#778899")
copyLabel.pack(side="right")
# ---------------------------------------------------


mainRoot.mainloop()
