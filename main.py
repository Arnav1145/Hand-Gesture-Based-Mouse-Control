# Import the necessary modules
import tkinter as tk
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import numpy as np
import time
import autopy
import pyautogui
import mouse_and_drawing as md


# Create the Customtkinter app instance
app = ctk.CTk()
app.bind('<Escape>', lambda e: app.quit())


cap = cv2.VideoCapture(0)

width, height =  640, 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


label_widget = tk.Label(app)
label_widget.pack()

# Set the title of the window
app.title("Hand Gesture Based Mouse Control")

# Set the size of the window
app.geometry("1000x500")

def button_click():
    # Capture the video frame by frame
    _, frame = cap.read()

    frame = md.open_camera(frame)

    # Convert image from one color space to other
    opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    # Capture the latest frame and transform to image
    captured_image = Image.fromarray(opencv_image)

    # Convert captured image to photoimage
    photo_image = ImageTk.PhotoImage(image=captured_image)

    # Displaying photoimage in the label
    label_widget.photo_image = photo_image

    # Configure image in the label
    label_widget.configure(image=photo_image)

    # Repeat the same process after every 10 seconds
    label_widget.after(10, button_click)




# Create the container frame
container = tk.Frame(app)
container.pack(fill=tk.BOTH, expand=True)

# Create the left column frame
left_frame = tk.Frame(container, bg="#222831", width=300)
left_frame.pack(side="left", fill="y")

# Create the right column frame
right_frame = tk.Frame(container, bg="#2D4059", padx=10, pady=10)
right_frame.pack(side="left", fill="both", expand=True)


################################################################
# Create the home page frame
home_page = tk.Frame(right_frame, bg="#2D4059")
home_page.pack(fill="both", expand=True)

# Load the background image for the home page
background_image = Image.open("assets/homePageImage.jpg")
resized_image = background_image.resize((home_page.winfo_width(), home_page.winfo_height()), Image.Resampling.LANCZOS)
background_image = ImageTk.PhotoImage(resized_image)


# Create a label with the background image and pack it into the home page frame
background_label = tk.Label(home_page, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a label for the welcome message and place it on top of the background label
welcome_label = tk.Label(background_label, text="Welcome to the future!!!", font=("Arial", 24, "bold"), fg="white",highlightthickness=0, padx=20, pady=20)
welcome_label.place(relx=0.5, rely=0, anchor="n")

# Update the home page size when it changes
def update_home_page_size(event):
   # Update the size of the background image when the home page frame size changes
    global background_image
    background_image = Image.open("assets/homePageImage.jpg")
    background_image = background_image.resize((home_page.winfo_width(), home_page.winfo_height()), Image.Resampling.LANCZOS)
    background_image = ImageTk.PhotoImage(background_image)
    background_label.configure(image=background_image)

# Bind the update_home_page_size function to the home page frame's <Configure> event
home_page.bind("<Configure>", update_home_page_size)
################################################################

# Define a function to show the home page and hide other pages
def show_home_page():
    home_page.pack(fill="both", expand=True)
    # Hide other pages if they are visible
    if setting_page.winfo_ismapped():
        setting_page.pack_forget()
    if aboutUs_page.winfo_ismapped():
        aboutUs_page.pack_forget()


# Define a function to change the background color of the home button on mouse enter
def on_enter(button):
    button.config(bg="#2D4059")

# Define a function to change the background color of the home button on mouse leave
def on_leave(button):
    button.config(bg="#222831")

########################################
# Left frame buttons added from here
########################################

# Load the home icon image
home_icon = Image.open("assets\home.png")
home_icon = home_icon.resize((30, 30), Image.Resampling.LANCZOS)
home_icon = ImageTk.PhotoImage(home_icon)

# Create the home button with the home icon image
home_button = tk.Button(left_frame, image=home_icon,text=" Home",compound="left",font=("TkDefaultFont", 16), bg="#222831",fg="white", bd=0, padx=0, pady=0, command=show_home_page)
home_button.pack(side="top", padx=50, pady=50, anchor="w")
home_button.bind("<Enter>", lambda e: on_enter(home_button))
home_button.bind("<Leave>", lambda e: on_leave(home_button))

# Load the setting icon image
setting_icon = Image.open("assets\Setting.png")
setting_icon = setting_icon.resize((30, 30), Image.Resampling.LANCZOS)
setting_icon = ImageTk.PhotoImage(setting_icon)


# Create the setting button with the home icon image
setting_button = tk.Button(left_frame, image=setting_icon,text=" Setting",compound="left",font=("TkDefaultFont", 16), bg="#222831",fg="white", bd=0, padx=0, pady=0)
setting_button.pack(side="top", padx=50, pady=50, anchor="w")
setting_button.bind("<Enter>",lambda e: on_enter(setting_button))
setting_button.bind("<Leave>",lambda e: on_leave(setting_button))

# Load the about us icon image
aboutUs_icon = Image.open("assets\AboutUs.png")
aboutUs_icon = aboutUs_icon.resize((30, 30), Image.Resampling.LANCZOS)
aboutUs_icon = ImageTk.PhotoImage(aboutUs_icon)

# Create the setting button with the home icon image
aboutUs_button = tk.Button(left_frame, image=aboutUs_icon,text=" About Us",compound="left",font=("TkDefaultFont", 16), bg="#222831",fg="white", bd=0, padx=0, pady=0)
aboutUs_button.pack(side="top", padx=50, pady=50, anchor="w")
aboutUs_button.bind("<Enter>",lambda e: on_enter(aboutUs_button))
aboutUs_button.bind("<Leave>",lambda e: on_leave(aboutUs_button))

# Buttons are added
########################################


# Create a label with the header text and pack it into the header frame
header_label = tk.Label(right_frame, text="Hand Gesture Based Mouse Control", font=("TkDefaultFont", 16), bg="#2D4059", fg="white")
header_label.pack(fill="x", padx=0, pady=0,ipady=5)

button1 = tk.Button(app, text="Open Camera",command=button_click)
button1.pack()

# Hide the home page on startup
home_page.pack_forget()

# Show the header page on startup
header_label.pack(fill="x", padx=0, pady=0, ipady=5)


# Start the mainloop to display the GUI
app.mainloop()
