from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from functools import partial
import LoginFrame
import mysql.connector
from main import *
# -------------------------------------------------------------------

signup_image = None
signup_frame = None


def add_signup_UI(root):

    root.title("Sign Up - Owner's Only")

# ---------------------------------------------------------------------


# --------------------------------------------------------------------

    image = PhotoImage(file="../UI/images/signup.png")

    global signup_image
    global signup_frame

    signup_image = Label(root, image=image, border=0, bg="white")
    signup_image.image = image
    signup_image.place(x=40, y=130)

    signup_frame = Frame(root, name="signup", width=450,
                         height=520, bg='white')
    signup_frame.place(x=520, y=140)

    head = Label(signup_frame, text=" Owner Sign Up", fg="#2B3467", bg="white", font=(
        "Microsoft Yahei UI Light", 23, 'bold')).place(x=115, y=18)
# ------------------------------------------------------------

    def on_enter(e):
        c = e.widget
        if c.get() == 'Full Name' or c.get() == 'Username' or c.get() == 'Password' or c.get() == 'Confirm Password':
            e.widget.delete(0, 'end')

    def on_leave(e):
        s = str(e.widget)
        if s == '.signup.username' and e.widget.get() == "":
            e.widget.insert(0, 'Username')
        elif s == '.signup.password' and e.widget.get() == "":
            e.widget.insert(0, 'Password')
        elif s == '.signup.fullname' and e.widget.get() == "":
            e.widget.insert(0, 'Full Name')
        elif s == '.signup.confirmpassword' and e.widget.get() == "":
            e.widget.insert(0, 'Confirm Password')

# =--------------------------------------------------------------------------
    name = Entry(signup_frame, width=30, name='fullname', fg="black",
                 border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    name.place(x=120, y=120)
    name.insert(0, 'Full Name')
    name.bind("<FocusIn>", on_enter)
    name.bind("<FocusOut>", on_leave)

    Frame(signup_frame, width=250, height=2, bg='#BAD7E9').place(x=115, y=147)

# ------------------------------------------------------------

    user = Entry(signup_frame, width=30, fg="black",  border=0,
                 name='username', bg='white', font=('Microsoft Yahei UI Light', 11))
    user.place(x=120, y=200)
    user.insert(0, 'Username')
    user.bind("<FocusIn>", on_enter)
    user.bind("<FocusOut>", on_leave)

    Frame(signup_frame, width=250, height=2, bg='#BAD7E9').place(x=115, y=227)


# ------------------------------------------------------------

    code = Entry(signup_frame, width=30, fg="black", name='password',
                 border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    code.place(x=120, y=280)
    code.insert(0, 'Password')
    code.bind("<FocusIn>", on_enter)
    code.bind("<FocusOut>", on_leave)

    Frame(signup_frame, width=250, height=2, bg='#BAD7E9').place(x=115, y=307)

# ------------------------------------------------------------

    conf_code = Entry(signup_frame, name='confirmpassword', width=30, fg="black",
                      border=0, bg='white', font=('Microsoft Yahei UI Light', 11))
    conf_code.place(x=120, y=360)
    conf_code.insert(0, 'Confirm Password')
    conf_code.bind("<FocusIn>", on_enter)
    conf_code.bind("<FocusOut>", on_leave)

    Frame(signup_frame, width=250, height=2, bg='#BAD7E9').place(x=115, y=387)

# ------------------------------------------------
    signup_btn = Button(signup_frame, width=30, pady=6, text="Sign Up", font=('Microsoft Yahei UI Light', 11), bg="#EB455F",
                        fg='white', cursor='hand2', border=0, command=partial(register_data, name, user, code, conf_code)).place(x=110, y=430)
    label = Label(signup_frame, text='I have an account', fg='black',
                  bg='white', font=("Microsoft Yahei UI Light", 9))
    label.place(x=170, y=490)

    signin = Button(signup_frame, width=6, text="Log in", border=0, bg='white', cursor='hand2',
                    fg='#EB455F', activebackground="white", command=partial(final_signup, root)).place(x=275, y=491)

# -----------------------------------------------------


def final_signup(root):
    remove_signup_UI()
    LoginFrame.add_login_UI(root)


def remove_signup_UI():
    signup_image.place_forget()
    signup_frame.place_forget()


# -----------------------------------------------------

def register_data(name, user, code, conf_code):
    lt = []
    lt = (name.get()).split(" ")
    if len(lt) < 2:
        messagebox.showerror("Error", "Enter Full Name")
    elif name.get() == "Full Name" or user.get() == "Username" or code.get() == "Password" or conf_code == "Confirm Password":
        messagebox.showerror('Error', "Enter Valid Details Only")
    elif name.get() == "" or user.get() == "" or code.get() == "" or conf_code == "":
        messagebox.showerror('Error', "All fields are required")
    elif len(user.get()) < 5 or len(code.get()) < 5:
        messagebox.showerror(
            'Error', "More than 4 characters required in Username and Password")
    elif code.get() != conf_code.get():
        messagebox.showerror('Error', "Both the Passwords do not match")
    else:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="Vedant@123", database='ddd')
        my_cursor = conn.cursor()
        query = ("select * from login where user = %s")
        value = (user.get(),)
        my_cursor.execute(query, value)
        row = my_cursor.fetchone()
        if row != None:
            messagebox.showerror(
                "Error", "User Already Exists. Use Another Username")
        else:
            my_cursor.execute("insert into login values (%s,%s,%s,%s)",
                              (name.get(), user.get(), code.get(), conf_code.get()))
            conn.commit()
            conn.close()
            messagebox.showinfo("Register Successful",
                                "User Registered Successfully")

# -------------------------------------------------------------------------------------------------------------

