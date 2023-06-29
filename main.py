from tkinter import *
from tkinter import colorchooser
from tkinter import messagebox
from mysql.connector import Connect, Error
import re, time, cv2
import mediapipe as mp
import pyautogui as pag
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# my mainroot part
# ----------------------------------------------------------------------
mainRoot=Tk()
mainRoot.iconbitmap('icons\\mainRoot.ico')
mainRoot.title('controlling system')

# ---------------------------------------------------
# size of main root
w=1000
h=1000
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

# my time value
pageTime=10
# control part
# -------------------------------
mosueClickSens=0.01
volumeMoveSense=2
def control(event):
    # our main program for controlling the computer
    def mainProgram():
        def justMouse(event):
            # reading camera
            cam=cv2.VideoCapture(0)
            # read time for set timer for the camera reading
            firstTime=time.time()
            # get our AI for face detection
            faceDetector=mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
            # make on loop for work on frames
            while True:
                # time condition
                if time.time() - firstTime >= pageTime:
                    cv2.destroyAllWindows()
                    break  
                # reading the camera 
                _, frame=cam.read()
                # get shape for our sizing
                frameY, frameX, _=frame.shape
                frame=cv2.flip(frame, 1)
                # change color for better process
                progressImg=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                outputImg=faceDetector.process(progressImg)
                screenw, screenh=pag.size()
                # get landmarks for progressing
                outputlandmarks=outputImg.multi_face_landmarks
                if outputlandmarks:
                    landmarks=outputlandmarks[0].landmark
                    # get right eye landmarks for progress
                    for lid, landmark in enumerate(landmarks[474:478]):
                        x=int(landmark.x* frameX)
                        y=int(landmark.y* frameY)
                        # draw circle for the right eye
                        cv2.circle(frame, (x,y), 3, (0,255,0))
                        # mouse moving part
                        if lid == 1:
                            mX=landmark.x*screenw
                            mY=landmark.y*screenh
                            pag.moveTo(mX,mY)
                    # get landmark for click
                    clickList=[landmarks[145], landmarks[159]]
                    # clicking part
                    if(clickList[0].y - clickList[1].y < mosueClickSens):
                        pag.click()
                        pag.sleep(1)
                cv2.imshow('mouse program', frame)
                cv2.waitKey(1)
        def justVolume(event):
            # open the camera
            cam=cv2.VideoCapture(0)
            startTime=time.time()
            
            # my hand find class for better and faster access
            class handDetector:
                def __init__(self, mode=False, maxHands=2, detectionCon=1, trackCon=0.5):
                    self.m=mode
                    self.mh=maxHands
                    self.dc=detectionCon
                    self.tc=trackCon
                    
                    # AI for analysis the hand and control it
                    self.AIhand=mp.solutions.hands
                    self.hands=self.AIhand.Hands(self.m, self.mh, self.dc, self.tc)
                    self.AIdraw=mp.solutions.drawing_utils

                # my hand finder and drawer
                def findHands(self, image, draw=True):
                    changedColorimage=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    self.answer=self.hands.process(changedColorimage)
                    # our drawer for hand
                    if self.answer.multi_hand_landmarks:
                        for landmark in self.answer.multi_hand_landmarks:
                            if draw:
                                self.AIdraw.draw_landmarks(image, landmark, self.AIhand.HAND_CONNECTIONS)
                    return image
                # our function for return y of landmark for control  
                # and control volume with it
                def findLandmarkPosition(self, img, handNo=0, draw=True):
                    if self.answer.multi_hand_landmarks:
                        hand=self.answer.multi_hand_landmarks[handNo]
                        for landmarkId, landmark in enumerate(hand.landmark):
                            h,_ ,_ =img.shape
                            if landmarkId==1:
                                return float(landmark.y * h)

            # our speaker part
            devices=AudioUtilities.GetSpeakers()
            interface=devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume=cast(interface, POINTER(IAudioEndpointVolume))
            
            # my setter part for volume
            setterVolume=-15.0  
            volume.SetMasterVolumeLevel(setterVolume, None)
            firstPosition=0
            firstTime=True
            
            # my class for search the hands
            handAgent=handDetector()     
            
            while True:
                # my break time
                if time.time()-startTime > pageTime:
                    cv2.destroyAllWindows()
                    break
                # get frame from camera
                _, frame=cam.read()
                frame=cv2.flip(frame, 1)
                
                # my agent for find hand and get dta from it to change
                frame=handAgent.findHands(frame)
                # i fit is first time, it will just add the hand data
                # to one value for control in next parts
                if firstTime:
                    firstPosition=handAgent.findLandmarkPosition(frame)
                    firstTime=False
                else:
                    # our hand control part, if it get lower and higher, change the volume
                    if handAgent.findLandmarkPosition(frame):
                        now=handAgent.findLandmarkPosition(frame)
                        if (now - firstPosition) < -3:
                            if setterVolume < 0:
                                setterVolume+=volumeMoveSense
                                volume.SetMasterVolumeLevel(setterVolume, None)
                        elif (now - firstPosition) > 3:
                            if setterVolume > -65:
                                setterVolume-=volumeMoveSense
                                volume.SetMasterVolumeLevel(setterVolume, None)
                        firstPosition=now
                cv2.imshow('volume control', frame)
                cv2.waitKey(1)
        # our main program root
        mainProgramRoot=Tk()
        mainProgramRoot.title('controling program')
        mainProgramRoot.iconbitmap('icons/mainProgramRoot.ico')
        mainProgramRoot.geometry('%dx%d+%d+%d'%(1000,400,1500,1100))
        
        # our wellcome label for main program page
        welcomeLabel=Label(master=mainProgramRoot, text='Welcome to the control program')
        welcomeLabel.pack()
        
        hintLabel=Label(    
                        master=mainProgramRoot,
                        text='you can choose mouse or volume control or both of them\nhint: if you set both, program will lose performance'
                        
                        )
        hintLabel.pack()
        
        justMouseControl=Button(master=mainProgramRoot, text='mouse control', bg='#FFF5EE')
        justMouseControl.bind('<Enter>', lambda event: justMouseControl.config(bg='#F3E5AB'))
        justMouseControl.bind('<Leave>', lambda event: justMouseControl.config(bg='#FFF5EE'))
        justMouseControl.bind('<Button>', justMouse)
        justMouseControl.pack()
        
        
        justVolumeControl=Button(master=mainProgramRoot, text='volume control', bg='#FFF5EE')
        justVolumeControl.bind('<Enter>', lambda event: justVolumeControl.config(bg='#F3E5AB'))
        justVolumeControl.bind('<Leave>', lambda event: justVolumeControl.config(bg='#FFF5EE'))
        justVolumeControl.bind('<Button>', justVolume)
        justVolumeControl.pack()
        
        mainProgramRoot.mainloop()
    # a variable for set true or false result
    isOk=False
    # get data
    controlName=nameEntry.get()
    controlPass=passEntry.get()
    # controlling part
    if re.search(r'\d\D+', controlName):
        messagebox.showerror('Error', 'username can\'t have number in first or middle of name')
    elif controlName=='' or controlPass=='':
        messagebox.showerror('Error', 'uername or password can\'t be empty')  
    else:
        try:
            with Connect(user='root', port=3306, password='Yasharzavary360', database='computercontrol') as conn:
                sqlCursor=conn.cursor(buffered=True)
                sqlCursor.execute("select * from person")
                for i in sqlCursor:
                    if i[2]==controlName and i[3]==controlPass:
                        isOk=True
                        break
                conn.commit()
        except Error as err:
            messagebox.showinfo('info', 'connection with server is lost...please try again later')
            print(err)
        if isOk:
            mainProgram()
        else:
            messagebox.showerror('Error', 'password or username is incorrect')
        
    
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
        # my background color changer
        colorCode=colorchooser.askcolor(title="choose color")
        mainRoot.config(bg=colorCode[1])
        nameLabel.config(bg=colorCode[1])
        passLabel.config(bg=colorCode[1])
    def selectMouseSensivity(event):
        def Senscontrol(event):
            newSens=newSensEntry.get()
            def changer():
                global mosueClickSens
                mosueClickSens=float(newSens)
            if newSens=='':
                messagebox.showerror('Error', 'sens can\'t be empty')  
            elif re.search(r"[!\"#$%&'()*,/:;<=>?@[\]^_`{|}~ A-z a-z]", newSens):
                messagebox.showerror('Error', 'your sens must be numeric')
            elif float(newSens) > 1 or float(newSens) < 0:
                messagebox.showerror('Error', 'your sens must be in range 0-1')
            else:
                changer()
        # mouse sensitivity root
        mouseSensRoot=Tk()
        mouseSensRoot.title('sens change')
        mouseSensRoot.geometry('%dx%d+%d+%d'%(600,200,400,900))
        mouseSensRoot.iconbitmap('icons\\mouseset.ico')
        
        newSensFrame=Frame(master=mouseSensRoot)
        newSensFrame.pack(side='top')
        
        # my new sens label
        newSensLabel=Label(master=newSensFrame, text='new sensitivity(<1): ')
        newSensLabel.pack(side='left')
        
        # my sens entry
        newSensEntry=Entry(master=newSensFrame)
        newSensEntry.pack()
        
        # change button
        changeButton=Button(master=mouseSensRoot, text="change", bg="#FFF5EE")
        changeButton.bind("<Enter>", lambda event: changeButton.config(bg="#F3E5AB"))
        changeButton.bind("<Leave>", lambda event: changeButton.config(bg="#FFF5EE"))
        changeButton.bind("<Button>", Senscontrol)
        changeButton.pack()
        
        
        mouseSensRoot.mainloop()
    
    def selectVolumeSensivity(event):
        def changer(event):
            newSense=setVolumeEntry.get()
            if re.search(r'[^0-9]', newSense):
                messagebox.showerror('Error', 'you must use integer number for sense')
            else:
                try:
                    newSense=int(newSense)
                    if newSense > 65 or newSense < 0:
                        messagebox.showerror('Error', 'you must select integer number between 0 and 65')
                except Error as err:
                    print(err)
                    messagebox.showerror('Error','Error happened, please control your number')
        setVolumeRoot=Tk()
        setVolumeRoot.title('volume sense')
        setVolumeRoot.geometry('%dx%d+%d+%d'%(600,200,400,900))
        setVolumeRoot.iconbitmap('icons\\volumeset.ico')
           
        setVolumeLabel=Label(master=setVolumeRoot, text='set volume increase sense')
        setVolumeLabel.pack(side='top')
        
        
        setVolumeFrame=Frame(master=setVolumeRoot, width=600, height=40)
        setVolumeFrame.pack(side='top')
        setVolumeFrame.pack_propagate(0)
        
        setVolumeInfo=Label(master=setVolumeFrame, text='new sense(0 to 65) = ')
        setVolumeInfo.pack(side='left')
        
        setVolumeEntry=Entry(master=setVolumeFrame)
        setVolumeEntry.pack(side='right')
        
        setVolumeButton=Button(master=setVolumeRoot, text='change')
        setVolumeButton.bind("<Enter>", lambda event: setVolumeButton.config(bg="#F3E5AB"))
        setVolumeButton.bind("<Leave>", lambda event: setVolumeButton.config(bg="#FFF5EE"))
        setVolumeButton.bind("<Button>", changer)
        setVolumeButton.pack()
        
        setVolumeRoot.mainloop()
    
    
    # setRoot 
    setRoot=Tk()
    setRoot.title("setting")
    setRoot.iconbitmap("icons\\setting.ico")
    
    w=400
    h=400
    setRoot.geometry("%dx%d+%d+%d"%(w,h,500,600))
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
copyFrame=Frame(master=mainRoot, bg="#778899", width=1000, height=40)
copyFrame.pack(side="bottom")
copyFrame.pack_propagate(0)

# copyright label
copyLabel=Label(master=copyFrame, text="@copyright-YasharZavaryRezaie-2023", bg="#778899")
copyLabel.pack(side="right")
# ---------------------------------------------------
# ---------------------------------------------------
# sign up part
def signUp(event):
    signUpRoot=Tk()
    signUpRoot.title("Sign Up")
    signUpRoot.iconbitmap("icons\\signUp.ico")
    w=700
    h=700
    signUpRoot.geometry("%dx%d+%d+%d"%(w, h , 2500, 800))
    
    # ---------------------------------------------------
    # name frame and label
    newNameFrame=Frame(master=signUpRoot, width=700, height=30)
    newNameFrame.pack(side="top")
    
    newNameLabel=Label(master=newNameFrame, text="Full name:")
    newNameLabel.pack(side="left")
    
    newNameEntry=Entry(master=newNameFrame)
    newNameEntry.pack(side="left")
    # ---------------------------------------------------
    # ---------------------------------------------------
    # user name part
    
    newUserNameFrame=Frame(master=signUpRoot, width=700, height=30)
    newUserNameFrame.pack(side="top")
    
    newUserNameLabel=Label(master=newUserNameFrame, text="User name:")
    newUserNameLabel.pack(side="left")
    
    newUserNameEntry=Entry(master=newUserNameFrame)
    newUserNameEntry.pack(side="left")
    
    # ---------------------------------------------------
    # ---------------------------------------------------
    # new password entry
    
    newPassFrame=Frame(master=signUpRoot, width=700, height=30)
    newPassFrame.pack(side="top")
    
    newPassLabel=Label(master=newPassFrame, text="password:")
    newPassLabel.pack(side="left")
    
    newPassEntry=Entry(master=newPassFrame)
    newPassEntry.pack(side="left")
    # -----------------------------------------------------
    # -----------------------------------------------------
    # mobile phone entry
    newPhoneFrame=Frame(master=signUpRoot, width=700, height=30)
    newPhoneFrame.pack(side="top")
    
    newPhoneLabel=Label(master=newPhoneFrame, text="phone number: +98")
    newPhoneLabel.pack(side="left")
    
    newPhoneEntry=Entry(master=newPhoneFrame)
    newPhoneEntry.pack(side="left")
    # -----------------------------------------------------
    def signUpControl(event):
        # get data's of user
        username=newUserNameEntry.get()
        fullname=newNameEntry.get()
        password=newPassEntry.get()
        phone=newPhoneEntry.get()
        
        # --------------------------------------------------------
        # control them with standards
        if username=="" or password=="" or phone=="" or fullname=="":
            messagebox.showerror('Error', 'slots can\'t be empty')
        elif re.search(r"\d", fullname):
            messagebox.showerror('Error', 'you\'r name can\'t have number in it' )
        elif re.search(r"\d\D+", username):
            messagebox.showerror('Error', 'you can\'t write number in first or middle of your user name')
        elif len(phone)!=10 or re.search(r'\D', phone):
            messagebox.showerror('Error', 'phone number is invalid')
        # -----------------------------------------------------------
        else:
            # if everything is ok, it come to here
            try:
                # connecting to the database to add new user
                with Connect(user="root", port=3306, password="Yasharzavary360", database='computercontrol') as conn:
                    sqlcursor=conn.cursor()
                    sqlcursor.execute('select * from person')
                    noError=True
                    # control that the new person's data not in the database
                    # ------------------------------------------------------------
                    for i in sqlcursor:
                        if i[2]==username:
                            messagebox.showinfo('Hint', 'username is already sign up')
                            noError=False
                            break
                        if i[4]==phone:
                            messagebox.showinfo('Hint', 'this phone number is already registered')
                            noError=False
                            break
                    # -----------------------------------------------------------
                    # -----------------------------------------------------------
                    if noError:
                        sqlcursor.execute('select max(idCode) from person')
                        # get max id for set new person's id code
                        for i in sqlcursor:
                            maxId=i[0]+1
                        
                        # our adding part for the new person
                        query="""insert into person (idCode, fullName, userName, pPassword, cellphoneNum)
                                values(%s,%s,%s,%s,%s)
                                """
                        addList=[(maxId, fullname, username, password, phone)]
                        sqlcursor.executemany(query, addList)
                        messagebox.showinfo('success', 'sign up successfully done')
                    conn.commit()  
                    # ------------------------------------------------------------
            # our error part for the server part 
            except Error as err:
                messagebox.showerror('Error', 'we can\'t connect to the server, please try again later')
                print(err)
    
    OkButton=Button(master=signUpRoot, text="sign up")
    OkButton.bind("<Enter>", lambda event: OkButton.config(bg="#F3E5AB"))
    OkButton.bind("<Leave>", lambda event: OkButton.config(bg="#FFF5EE"))
    OkButton.bind("<Button>", signUpControl)
    OkButton.pack()
    
    
    
    signUpRoot.mainloop()

# signup frame
signUpFrame=Frame(master=mainRoot, width=1000, height=60)
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


mainRoot.mainloop()
