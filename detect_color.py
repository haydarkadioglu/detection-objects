"""
-when open camera your should press 'a' for select ROI,
take in rectangle color for detect and press space or enter for verify ROI

-you can press 'c' for clear rectangle and select ROI again

-press 'q' for close camera

-now only detect blue-green-red
"""


import cv2 as cv
import numpy as np

vid = cv.VideoCapture(0)

vid.set(3,1280)
vid.set(4,720)

red_lower = np.array([136, 87, 111], np.uint8)
red_upper = np.array([180, 255, 255], np.uint8)

green_lower = np.array([25, 52, 72], np.uint8)
green_upper = np.array([102, 255, 255], np.uint8)


blue_lower = np.array([94, 80, 2], np.uint8)
blue_upper = np.array([120, 255, 255], np.uint8)


def detectColor(frame, hsv):

    
    red_mask = cv.inRange(hsv, red_lower, red_upper)
    green_mask = cv.inRange(hsv, green_lower, green_upper)
    blue_mask = cv.inRange(hsv, blue_lower, blue_upper)

    
    kernal = np.ones((5, 5), "uint8")

    red_mask = cv.dilate(red_mask, kernal)
    green_mask = cv.dilate(green_mask, kernal)
    blue_mask = cv.dilate(blue_mask, kernal)
    
    cv.imshow('red_mask', red_mask)
    cv.imshow('green_mask', green_mask)
    cv.imshow('blue_mask', blue_mask)

    conr, _ = cv.findContours(red_mask, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    cong, _ = cv.findContours(green_mask, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    conb, _ = cv.findContours(blue_mask, cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)


    for contour in conr:
        area = cv.contourArea(contour)
        if(area > 350):
            cv.putText(frame, "Red Colour", (res[0], res[1]-10),
                cv.FONT_HERSHEY_COMPLEX, 1.0,(0, 0, 255))
    
    for contour in cong:
        area = cv.contourArea(contour)
        if(area > 350):
            cv.putText(frame, "Green Colour", (res[0], res[1]-50),
                cv.FONT_HERSHEY_COMPLEX, 1.0,(50, 255, 0))
    
    for contour in conb:
        area = cv.contourArea(contour)
        if(area > 350):
            cv.putText(frame, "Blue Colour", (res[0], res[1]-100),
                cv.FONT_HERSHEY_COMPLEX, 1.0,(255, 50, 25))




    return frame


ver = False
res = None
hsv = None

while 1:
    _, frame = vid.read()
    frame = cv.flip(frame, 1)
    key = cv.waitKey(1)
      


    if key == ord('a'):
        
        res = cv.selectROI('webcam', frame)

    if key == ord('c'):
        res = None
        hsv = None
        ver = False
        
    if res != None:
        cropped = frame[int(res[1]):int(res[1]+res[3]),
                                int(res[0]):int(res[0]+res[2])]
        x,y,z = cropped.shape[::]

        cv.rectangle(frame, (res[0], res[1]), (res[0]+y, res[1]+x), (0,0,0), 1)
        hsv = cv.cvtColor(cropped, cv.COLOR_BGR2HSV)
        ver = True

    if ver == True:
        frame = detectColor(frame, hsv)

    cv.imshow('webcam', frame)

    if key==ord('q'):
        break


vid.release()
cv.destroyAllWindows()

