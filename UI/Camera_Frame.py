from tkinter import *
from tkinter import messagebox
from PIL import ImageTk
from PIL import Image
from LoginFrame import *
from SignupFrame import *
from main import *
from functools import partial
from OptionsFrame import *
import cv2
import os
from keras.models import load_model
import numpy as np
from pygame import mixer
import time
import imutils
# -------------------------------------------------------------------------------

# Loading Sound Files, Cascade files
mixer.init()
sound = mixer.Sound("../ring.wav")


# Declaring Global Variables
livet_frame = None
cap = None
camera_Label = None
cam_on = False
overlay = None
toggle_btn = None
subtitle_image = None
title_image = None
rec_frame = None



face = cv2.CascadeClassifier('..\\haar cascade files\\haarcascade_frontalface_alt.xml')
leye = cv2.CascadeClassifier('..\\haar cascade files\\haarcascade_lefteye_2splits.xml')
reye = cv2.CascadeClassifier('..\\haar cascade files\\haarcascade_righteye_2splits.xml')



lbl=['Close','Open']

model = load_model('../model.h5')
path = os.getcwd()
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
count=0
score=0
thicc=2
rpred=[99]
lpred=[99]






# -------------------------------------------------------------------------------
# Creating UI For the Frame
def add_Camera_UI(root, name, no):
    txt = f"Live Camera Feed : {name} , ID : {str(no)}"
    root.title(txt)

    global livet_frame, camera_Label, overlay, rec_frame

    # Title Image
    title = ImageTk.PhotoImage(file="../UI/images/title.png")
    title_image = Label(root, image=title, border=0)
    title_image.image = title
    title_image.place(x=0, y=10)

    rec_frame = Frame(root, name='rec', bg = 'white', width = 1000, height=110, border=0)
    rec_frame.place(x=0, y=105)
    # Subtitle Image
    image = ImageTk.PhotoImage(file="../UI/images/rec.png")
    subtitle_image = Label(rec_frame, image=image, border=0, bg="white")
    subtitle_image.image = image
    subtitle_image.place(x=0, y=0)

    # Frame for Camera I/O
    livet_frame = Frame(root, name='camera', bg='white',
                        width=910, height=485, border=0, )
    livet_frame.place(x=40, y=210)


    naam = "Driver Name : " + str(name)
    driver_name = Label(livet_frame, name = "name", bg= "white", text = naam, border = 0, font=("Microsoft Yahei UI Light", 14, 'bold'))
    driver_name.place(x= 550, y = 180)
    
    id1 = "ID : " + str(no)
    driver_id = Label(livet_frame, name = "id", bg= "white", text =id1, border = 0, font=("Microsoft Yahei UI Light", 14, 'bold'))
    driver_id.place(x= 550, y = 250)
    nu = str(no)

    # Frame Heading
    frame_head = Label(livet_frame, name="head", bg="white", fg="black",
                       text="Live Camera", border=0, font=("Microsoft Yahei UI Light", 18, 'bold'))
    frame_head.place(x=175, y=5)

    # Label for Camera Feed
    camera_Label = Label(livet_frame)

    # Overlay when Camera is Off
    overlay = Label(livet_frame, name="live", bg="black",
                    width=70, height=25, border=0)
    overlay.place(x=10, y=50)

    # Button for Camera
    global toggle_btn
    toggle_btn = Button(livet_frame, width=7, text="Start", border=1, font=("Microsoft Yahei UI Light", 10, 'bold'),
                      bg='white', cursor='hand2', fg='teal', activebackground="white", command=partial(toggle_camera, nu))
    toggle_btn.place(x=552, y=320)


    logout_btn = Button(livet_frame, width=7, text="Log Out", border=0,
                        bg='white', cursor='hand2', fg='#EB455F', activebackground = "white", command= partial(logout_action, root))
    logout_btn.place(x=820, y= 400)
# ------------------------------------------------------------------------------------ #


# Function for Making Predictions
def predict():
    global cam_on, face,leye, reye, lbl, model, path, count, score, thicc, rpred, lpred


    if cam_on:
        global cap, camera_Label
        
        ret, frame = cap.read()
        
        if ret:
            frame = cv2.flip(frame, 1)
            frame = imutils.resize(frame, width=490)
            
            height,width = frame.shape[:2] 

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            faces = face.detectMultiScale(gray,minNeighbors=5,scaleFactor=1.1,minSize=(25,25))
            left_eye = leye.detectMultiScale(gray)
            right_eye =  reye.detectMultiScale(gray)

            cv2.rectangle(frame, (0,height-50) , (200,height) , (0,0,0) , thickness=cv2.FILLED )

            for (x,y,w,h) in faces:
                cv2.rectangle(frame, (x,y) , (x+w,y+h) , (100,100,100) , 1 )

            for (x,y,w,h) in right_eye:
                r_eye=frame[y:y+h,x:x+w]
                count=count+1
                r_eye = cv2.cvtColor(r_eye,cv2.COLOR_BGR2GRAY)
                r_eye = cv2.resize(r_eye,(24,24))
                r_eye= r_eye/255
                r_eye=  r_eye.reshape(24,24,-1)
                r_eye = np.expand_dims(r_eye,axis=0)
                rpred = np.argmax(model.predict(r_eye),axis=-1)
                if(rpred[0]==1):
                    lbl='Open' 
                if(rpred[0]==0):
                    lbl='Closed'
                break

            for (x,y,w,h) in left_eye:
                l_eye=frame[y:y+h,x:x+w]
                count=count+1
                l_eye = cv2.cvtColor(l_eye,cv2.COLOR_BGR2GRAY)  
                l_eye = cv2.resize(l_eye,(24,24))
                l_eye= l_eye/255
                l_eye=l_eye.reshape(24,24,-1)
                l_eye = np.expand_dims(l_eye,axis=0)
                lpred = np.argmax(model.predict(l_eye),axis=-1)
                if(lpred[0]==1):
                    lbl='Open'   
                if(lpred[0]==0):
                    lbl='Closed'
                break

            if(rpred[0]==0 and lpred[0]==0):
                score=score+1
                cv2.putText(frame,"Closed",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
            # if(rpred[0]==1 or lpred[0]==1):
            else:
                score=score-1
                cv2.putText(frame,"Open",(10,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
            
                
            if(score<0):
                score=0   
            cv2.putText(frame,'Score:'+str(score),(100,height-20), font, 1,(255,255,255),1,cv2.LINE_AA)
            if(score>30):
                #person is feeling sleepy so we beep the alarm
                # cv2.imwrite(os.path.join(path,'image.jpg'),frame)
                try:
                    sound.play()
                    
                except:  # isplaying = False
                    pass
                if(thicc<16):
                    thicc= thicc+2
                else:
                    thicc=thicc-2
                    if(thicc<2):
                        thicc=2
                cv2.rectangle(frame,(0,0),(width,height),(0,0,255),thicc)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img1 = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img1)
            camera_Label.place(x=10, y=50)
            camera_Label.imgtk = imgtk
            camera_Label.configure(image=imgtk)
        camera_Label.after(20, predict)
        

# Function to Toggle Camera On/Off
def toggle_camera(no):
    global cam_on, cap, overlay, toggle_btn

    if not cam_on:
        cam_on = True
        toggle_btn.configure(text="Stop")
        if (no == '001'):
            cap = cv2.VideoCapture(1)
        elif(no == '002'):
            cap = cv2.VideoCapture(0)
        overlay.place_forget()
        predict()
    else:
        cam_on = False
        toggle_btn.configure(text="Start")

        if camera_Label:
            camera_Label.place_forget()
            overlay.place(x=10, y=50)

        if cap:
            cap.release()


# -------------------------------------------------------------------------------------------
def final_options(root):
    remove_options_UI()
    LoginFrame.add_login_UI(root)



# -------------------------------------------------------------------------------------------
def remove_options_UI():
    global rec_frame
    global livet_frame
    rec_frame.place_forget()
    livet_frame.place_forget()



# -------------------------------------------------------------------------------------------
def logout_action(root):
    open_main = messagebox.askyesno("Log Out", "Are You Sure?")
    if open_main > 0:
        remove_options_UI()
        LoginFrame.add_login_UI(root)
    else:
        if not open_main:
            return


# -------------------------------------------------------------------------------------------
if __name__ == "__main__":
    root = Tk()
    UI(root)
    # add_Camera_UI(root, "m", "002")
    root.mainloop()
