from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
from SignupFrame import *
import OptionsFrame
from main import *
import mysql.connector


# -----------------------------------------------------

login_image = None
main_frame = None


# --------------------------------------------------------

def add_login_UI(root):
    root.title("Log In - Owner's Only")
    image = ImageTk.PhotoImage(file="../UI/images/login.png")
    global login_image
    global main_frame

    login_image = Label(root, image=image, border=0, bg="white")
    login_image.image = image
    login_image.place(x=40, y=130)
    
    main_frame = Frame(root, name= 'login', bg='white', width=450, height=520, border =  0)
    main_frame.place(x=540, y=140)
        
    Label(main_frame, text="Log In", fg="#2B3467", bg="white",
          font=("Microsoft Yahei UI Light", 25, 'bold')).place(x=190, y=50)

    # --------------------------------------------------------------------
    def on_enter(e):
        c = e.widget
        if c.get() == 'Username' or c.get() == 'Password':
            e.widget.delete(0, 'end')

    def on_leave(e):
        s = str(e.widget)
        if s == '.login.username' and e.widget.get() == "":
            e.widget.insert(0, 'Username')
        elif s == '.login.password' and e.widget.get() == "":
            e.widget.insert(0, 'Password')
    # --------------------------------------------------------------------

    # --------------------------------------------------------------------
    user = Entry(main_frame, width=30, fg="black", border=0, bg='white',
                 name='username', font=('Microsoft Yahei UI Light', 11))
    user.place(x=120, y=160)
    user.insert(0, 'Username')
    user.bind("<FocusIn>", on_enter)
    user.bind("<FocusOut>", on_leave)

    Frame(main_frame, width=250, height=2, bg='#BAD7E9').place(x=115, y=187)
    # ---------------------------------------------------------------------

    # -------------------------------------------------------------------------------
    code = Entry(main_frame, width=30, fg="black", border=0,
                 name='password', bg='white', font=('Microsoft Yahei UI Light', 11))
    code.place(x=120, y=270)
    code.insert(0, 'Password')
    code.bind("<FocusIn>", on_enter)
    code.bind("<FocusOut>", on_leave)

    Frame(main_frame, width=250, height=2, bg='#BAD7E9').place(x=115, y=297)
    # --------------------------------------------------------------------------------

    # --------------------------------------------------------------------------------
    login_btn = Button(main_frame, width=30, pady=6, text="Log in", font=('Microsoft Yahei UI Light', 11), bg="#EB455F", fg='white', cursor='hand2', border=0, command = partial(login, user, code,root))
    login_btn.place(x=105, y=360)
    Label(main_frame, text='I don\'t have an account',

          fg='black', bg='white', font=("Microsoft Yahei UI Light", 9)).place(x=150, y=420)
    signup_btn = Button(main_frame, width=6, text="Sign Up", border=0,
                        bg='white', cursor='hand2', fg='#EB455F', activebackground = "white", command = partial(final_login, root))
    signup_btn.place(x=290, y=421)
    # --------------------------------------------------------------------------------


# ------------------------------------------------------------------

def login(user, code,root):
    if  user.get() == "" or code.get() == "":
        messagebox.showerror("Error", "All the Fields are Required")
    
    else: 
        conn = mysql.connector.connect(host="localhost", user="root", password="Vedant@123", database='ddd')
        my_cursor = conn.cursor()
        my_cursor.execute("select * from login where user=%s and code=%s", (user.get(), code.get()))
        row = my_cursor.fetchone()

        if row == None:
            messagebox.showerror("Error", "Invalid Username or Password")
        else:
            open_main = messagebox.askyesno("Login Successful", "Welcome User! Proceed?")
            if open_main>0:
                final_success(root)
            else:
                if not open_main:
                    return
        conn.commit()
        conn.close()



#------------------------------------------------------------------------------------------ 

def final_success(root):
    remove_login_UI()
    OptionsFrame.add_Options_UI(root)

def final_login(root):
    remove_login_UI()
    add_signup_UI(root)


def remove_login_UI():
    login_image.place_forget()
    main_frame.place_forget()



# -------------------------------------------------------------------------

