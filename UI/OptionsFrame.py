from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from LoginFrame import *
from SignupFrame import *
import Camera_Frame
from functools import partial
# ---------------------------------------------

options_image = None
options_frame = None


def add_Options_UI(root):
	root.title("Driver Selection")
	image = ImageTk.PhotoImage(file="../UI/images/options.png")
	global options_image
	global options_frame

	options_image = Label(root, image=image, border=0, bg="white")
	options_image.image = image
	options_image.place(x=40, y=130)
    
	options_frame = Frame(root, name= 'login', bg='white', width=450, height=520, border =  0)
	options_frame.place(x=540, y=140)

	head =Label(options_frame, text="Choose a Driver", fg= "#2B3467", bg ="white", font=("Microsoft Yahei UI Light", 25, 'bold'))
	head.place(x=90, y=90)
        
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
	# --------------------------------------------------------------------------------

	menu_list = {"--Select Driver--","001--Manish R.", "002--Raju D."}
	driver_id = StringVar()
	driver_id.set("--Select Driver--")
	drop= OptionMenu(options_frame, driver_id, *menu_list)
	drop.place(x=110,y=210)
	drop.config(font=("Microsoft Yahei UI Light", 11, 'bold'),width = 20, bg="white", border = 0)

	options_btn = Button(options_frame, width=22, pady=6, text="Confirm", font=('Microsoft Yahei UI Light', 12), bg="#EB455F", fg='white', cursor='hand2', border=0, command=partial(select_driver, driver_id,root)) 
	options_btn.place(x=125, y=320)



	logout_btn = Button(options_frame, width=6, text="Log Out", border=0,
                        bg='white', cursor='hand2', fg='#EB455F', activebackground = "white", command= partial(logout_action, root))
	logout_btn.place(x=205, y=380)
# -------------------------------------------------------------------------------------------


def final_options(root):
    remove_options_UI()
    LoginFrame.add_login_UI(root)


def remove_options_UI():
    options_image.place_forget()
    options_frame.place_forget()


def logout_action(root):
	open_main = messagebox.askyesno("Log Out", "Are You Sure?")
	if open_main > 0:
		remove_options_UI()
		LoginFrame.add_login_UI(root)
	else:
		if not open_main:
			return
	

def select_driver(driver_id,root):
	driver_no = driver_id.get().split("--")[0]
	driver_name = driver_id.get().split("--")[1]
	print(type(driver_no))
	if driver_name == "Select Driver":
		messagebox.showerror('Error', "Please Select a Driver")
	else:
		remove_options_UI()
		Camera_Frame.add_Camera_UI(root,driver_name, driver_no)

# ------------------------------------------------------------------------------------
if __name__ == "__main__":
	root = Tk()
	root.grid_propagate(False)
	UI(root)
	add_Options_UI(root)
	root.mainloop()