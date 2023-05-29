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





mainRoot.mainloop()
