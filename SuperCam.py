# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 13:54:40 2021

@author: chmn_victor
"""
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog

def click_event(event, x, y, flags, param):
    global switch
    
    if event == cv2.EVENT_LBUTTONDOWN:
        if switch==0:
            switch=1
            cv2.imshow("image", img)
        else:
            switch=0
            cv2.imshow("image", imgBis)
        

# Function for when the 'Select file' button is pushed
def button_push():
        global fullFileName
        global keepGoing
        fullFileName=""
        fullFileName=filedialog.askopenfilename(initialdir=folderName)
        if fullFileName!="":
            root.destroy()
            
def button_push2():
        global severalFiles
        global fullFileNames
        global keepGoing
        fullFileNames=""
        fullFileNames=filedialog.askopenfilenames(initialdir=folderName)
        severalFiles=1
        if fullFileNames!="":
            root.destroy()
        
# Function for when the 'Same file' button is pushed
def same_file():
    global keepGoing
    root.destroy()
    if fullFileName=="":
        keepGoing=0
        root.destroy()
        
# Function for when the window is closd
def on_closing():
    global keepGoing
    keepGoing=0
    root.destroy()
    
def closing():
    root.destroy()
    

#cv2.imwrite(save_name,imTemp2)

switch=0
folderName="D:/Users/victo/Desktop/"
fullFileName=""
fullFileName2=""
keepGoing=1
while 1:
    
    severalFiles=0
    # Create input window
    root=tk.Tk()
    appLogo = tk.PhotoImage(file = 'AppLogo.png')
    root.geometry("400x180")
    root.title("SuperCam Auto-Processing")
    root.iconphoto(False, appLogo)
    
    frame=tk.Frame(root)
    frame.pack()
    
    button = tk.Button(frame, text = "Select file", command = button_push)
    button.pack(pady=10)
    button = tk.Button(frame, text = "Select multiple files", command = button_push2)
    button.pack(pady=10)
    button2 = tk.Button(frame, text = "Use same file", command = same_file)
    button2.pack(pady=10)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()
    
    if keepGoing==0:
        break
    
    # images reading
    flat = cv2.imread("SuperCamFlat4.png")
    # flat normalization
    flat=flat/255
    
    if (severalFiles==0):
        img = cv2.imread(fullFileName)
        # window creation
        cv2.namedWindow('image', cv2.WINDOW_NORMAL)
        # image and flat multiplication
        imgBis=img.copy()
        imgBis=img.astype(np.float64)
        imgBis=cv2.multiply(imgBis,flat)
        # color correction
        imgBis[:, :, 0]=imgBis[:, :, 0]*0.994
        imgBis[:, :, 1]=imgBis[:, :, 1]*0.920
        imgBis[:, :, 2]=imgBis[:, :, 2]*1.103
        # image greyscale creation
        imgBis=imgBis.astype(np.uint8)
        ret,imgBis=cv2.threshold(imgBis,0,255,cv2.THRESH_TOZERO)
        grayImage = cv2.cvtColor(imgBis, cv2.COLOR_BGR2GRAY)
        # min and max luminance calculation
        minL=np.mean(grayImage[0:50,0:50].flatten())
        maxL=max(grayImage.flatten())
        # setting dark point
        imgBis=imgBis-minL
        ret,imgBis=cv2.threshold(imgBis,0,255,cv2.THRESH_TOZERO)
        # resetting the maximum luminance to its initial value
        imgBis=imgBis.astype(np.uint8)
        grayImage = cv2.cvtColor(imgBis, cv2.COLOR_BGR2GRAY)
        imgBis=imgBis.astype(np.float64)
        newMaxL=max(grayImage.flatten())
        imgBis=(maxL/newMaxL)*imgBis
        imgBis=imgBis.astype(np.uint8)
        # increase saturation
        imgHSV=cv2.cvtColor(imgBis, cv2.COLOR_BGR2HSV)
        imgHSV[:, :, 1]=imgHSV[:, :, 1]*1.3
        # showing result
        imgBis=cv2.cvtColor(imgHSV, cv2.COLOR_HSV2BGR)
        cv2.imshow("image", imgBis)
        cv2.resizeWindow("image", 800, 800)
        cv2.moveWindow("image", 0,0)
        
        # left click switches between result and original picture
        cv2.setMouseCallback("image", click_event)
        # Wait for a mouse input
        k=cv2.waitKey(0)
        # saving result when S is pressed
        if k==115:
            size=len(fullFileName)
            cv2.imwrite(fullFileName[:size-4]+"_VignetCorr.png",imgBis)
        cv2.destroyAllWindows()
    else:
        for nameTemp in fullFileNames:
            img = cv2.imread(nameTemp)
            # window creation
            # image and flat multiplication
            imgBis=img.copy()
            imgBis=img.astype(np.float64)
            imgBis=cv2.multiply(imgBis,flat)
            # color correction
            imgBis[:, :, 0]=imgBis[:, :, 0]*0.994
            imgBis[:, :, 1]=imgBis[:, :, 1]*0.920
            imgBis[:, :, 2]=imgBis[:, :, 2]*1.103
            # image greyscale creation
            imgBis=imgBis.astype(np.uint8)
            ret,imgBis=cv2.threshold(imgBis,0,255,cv2.THRESH_TOZERO)
            grayImage = cv2.cvtColor(imgBis, cv2.COLOR_BGR2GRAY)
            # min and max luminance calculation
            minL=np.mean(grayImage[0:20,0:20].flatten())
            maxL=max(grayImage.flatten())
            # setting dark point
            imgBis=imgBis-minL
            ret,imgBis=cv2.threshold(imgBis,0,255,cv2.THRESH_TOZERO)
            # resetting the maximum luminance to its initial value
            imgBis=imgBis.astype(np.uint8)
            grayImage = cv2.cvtColor(imgBis, cv2.COLOR_BGR2GRAY)
            imgBis=imgBis.astype(np.float64)
            newMaxL=max(grayImage.flatten())
            imgBis=(maxL/newMaxL)*imgBis
            imgBis=imgBis.astype(np.uint8)
            # increase saturation
            imgHSV=cv2.cvtColor(imgBis, cv2.COLOR_BGR2HSV)
            imgHSV[:, :, 1]=imgHSV[:, :, 1]*1.3
            imgBis=cv2.cvtColor(imgHSV, cv2.COLOR_HSV2BGR)
            # saving results
            size=len(nameTemp)
            cv2.imwrite(nameTemp[:size-4]+"_VignetCorr.png",imgBis)
           
        root.destroy()
        root=tk.Tk()
        appLogo = tk.PhotoImage(file = 'AppLogo.png')
        root.geometry("400x60")
        root.title("SuperCam Auto-Processing")
        root.iconphoto(False, appLogo)
        
        frame=tk.Frame(root)
        frame.pack()
        
        button = tk.Button(frame, text = "Files saved", command = closing)
        button.pack()
        root.protocol("WM_DELETE_WINDOW", on_closing)
        
        root.mainloop()
