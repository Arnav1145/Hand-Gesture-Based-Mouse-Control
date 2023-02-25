# Import the necessary modules
import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
import numpy as np
import time
import autopy
import pyautogui
import HandTrackingModule as htm


#variables
wCam, hCam = 640,480
wScr, hScr = autopy.screen.size()
frameR = 100 #Frame Reduction
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 5
# print(wScr, hScr)

#creating video capture object
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = htm.handDetector(maxHands=1)

# Create the Customtkinter app instance
app = ctk.CTk()
app.bind('<Escape>', lambda e: app.quit())

#label on which camera will be opened
label_widget = ctk.CTkLabel(app)
label_widget.pack()

#function to open or access camera
def open_camera():

    #1.Finde Hand Landmark
    global plocX, plocY
    success, frame = cap.read()
    frame = cv2.flip(frame,1)
    frame = detector.findHands(frame)
    lmlist, bbox = detector.findPosition(frame)

    #2.Get the tip of the index and middle finger
    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:]
        x2, y2 = lmlist[12][1:]
        # print(x1,y1,x2,y2)

        #3.check which fingers are up
        fingers = detector.fingersUp()
        cv2.rectangle(frame, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 3)
        # print(fingers)

        #4.Only Index Finger Moving mode
        if fingers[1]==1 and fingers[2]==0:
            # 5. Convert Coordinates
            x3 = np.interp(x1, (frameR,wCam-frameR), (0,wScr))
            y3 = np.interp(y1, (frameR,hCam-frameR), (0,hScr))

            # 6. smothen values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening
            # 7. Move Mouse
            autopy.mouse.move(clocX,clocY)
            plocX , plocY = clocX, clocY

        # 8. Both Index and middle fingers are up : clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            length, frame, _ = detector.findDistance(8,12,frame)
            # print(length)
            #click mouse if distance short
            if length < 40:
                autopy.mouse.click()
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
    label_widget.after(10, open_camera)

#created a function for hand gesture based mouse control
def virtual_mouse():
    print("Welcome!!!")



#created button when pressed open camera
button1 = ctk.CTkButton(app, text="Start",command=open_camera)
button1.pack()

# Set the title of the window
app.title("Hand Gesture Based Mouse Control")

# Set the size of the window
app.geometry("1000x500")


# Start the mainloop to display the GUI
app.mainloop()

