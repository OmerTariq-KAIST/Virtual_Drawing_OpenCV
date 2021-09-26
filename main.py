from handTracker import *
import cv2
import mediapipe as mp
import numpy as np


#initilize the habe detector
detector = HandTracker(detectionCon=0.8)

#initilize the camera 
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# creating canvas to draw on it
canvas = np.zeros((720,1280,3), np.uint8)

# define a previous point to be used with drawing a line
px,py = 0,0
color = (255,0,0)
#####
brushSize = 5
eraserSize = 20
####
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    detector.findHands(frame)
    positions = detector.getPostion(frame, draw=False)
    upFingers = detector.getUpFingers(frame)
    if upFingers:
        if upFingers[1] and upFingers[2]:
            px, py = 0, 0
            ####### chose a color for drawing #######
            #blue
            if 400<positions[8][0]<500 and 0<positions[8][1]<100:
                color = (255,0,0)
            #green
            elif 500<positions[8][0]<600 and 0<positions[8][1]<100:
                color = (0,255,0)
            #red
            elif 600<positions[8][0]<700 and 0<positions[8][1]<100:
                color = (0,0,255)
            #yellow
            elif 700<positions[8][0]<800 and 0<positions[8][1]<100:
                color = (0,255,255)
            #Eraser
            elif 800<positions[8][0]<900 and 0<positions[8][1]<100:
                color = (0,0,0)
            #Clear 
            elif 900<positions[8][0]<1000 and 0<positions[8][1]<100:
                canvas = np.zeros((720,1280,3), np.uint8)
            
            ##### pen sizes ######
            elif 1100<positions[8][0]<1200 and 50<positions[8][1]<150:
                brushSize = 5
            elif 1100<positions[8][0]<1200 and 150<positions[8][1]<250:
                brushSize = 10
            elif 1100<positions[8][0]<1200 and 250<positions[8][1]<350:
                brushSize = 15
            elif 1100<positions[8][0]<1200 and 350<positions[8][1]<450:
                brushSize = 20
            

        elif upFingers[1] and not upFingers[2]:
            #print('index finger is up')
            cv2.circle(frame, positions[8], brushSize, color,-1)
            #drawing on the canvas
            if px == 0 and py == 0:
                px, py = positions[8]
            if color == (0,0,0):
                cv2.line(canvas, (px,py), positions[8], color, eraserSize)
            else:
                cv2.line(canvas, (px,py), positions[8], color,brushSize)
            px, py = positions[8]

    ########### moving the draw to the main image #########
    canvasGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(canvasGray, 20, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, imgInv)
    frame = cv2.bitwise_or(frame, canvas)


    ########## pen colors' boxes #########
    #blue
    cv2.rectangle(frame, (400,0), (500, 100), (255,0,0), -1)
    #green
    cv2.rectangle(frame, (500,0), (600, 100), (0,255,0), -1)
    #red
    cv2.rectangle(frame, (600,0), (700, 100), (0,0,255), -1)
    #yellow
    cv2.rectangle(frame, (700,0), (800, 100), (0,255,255), -1)
    #Ereaser
    cv2.rectangle(frame, (800,0), (900, 100), (0,0,0), -1)
    cv2.putText(frame, "Ereaser", (820,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    #Clear All
    cv2.rectangle(frame, (900,0), (1000, 100), (100,100,100), -1)
    cv2.putText(frame, "Clear", (920,50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

    ########## brush size boxes ######
    #pen
    cv2.rectangle(frame, (1100,0), (1200, 50), color, -1)
    cv2.rectangle(frame, (1100,0), (1200, 50), (255,255,255), 2)
    cv2.putText(frame, "Pen", (1120,25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    #5
    cv2.rectangle(frame, (1100,50), (1200, 150), (150,150,150), -1)
    cv2.rectangle(frame, (1100,50), (1200, 150), (255,255,255), 2)
    cv2.putText(frame, "5", (1120,100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    #10
    cv2.rectangle(frame, (1100,150), (1200, 250), (150,150,150), -1)
    cv2.rectangle(frame, (1100,150), (1200, 250), (255,255,255), 2)
    cv2.putText(frame, "10", (1120,200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    #15
    cv2.rectangle(frame, (1100,250), (1200, 350), (150,150,150), -1)
    cv2.rectangle(frame, (1100,250), (1200, 350), (255,255,255), 2)
    cv2.putText(frame, "15", (1120,300), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
    #20
    cv2.rectangle(frame, (1100,350), (1200, 450), (150,150,150), -1)
    cv2.rectangle(frame, (1100,350), (1200, 450), (255,255,255), 2)
    cv2.putText(frame, "20", (1120,400), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)


    cv2.imshow('video', frame)
    #cv2.imshow('canvas', canvas)
    k= cv2.waitKey(1)
    if k == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()