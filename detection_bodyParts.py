"""
-anything detection is done on the haarcascade file; that's why if, if you change '.xml' file you can take different results 
"""

import cv2 as cv   

face = "Haarcascade\\haarcascade_frontalface_alt.xml"
facet = "Haarcascade\\haarcascade_profileface.xml"
faced = "Haarcascade\\haarcascade_frontalface_default.xml"
eye = "Haarcascade\\haarcascade_eye.xml"
smile = "Haarcascade\\haarcascade_smile.xml"

vid = cv.VideoCapture(0)

cascade = cv.CascadeClassifier(face)


while True:
    
    ret, frame = vid.read()
    frame = cv.flip(frame, 1)
    if cv.waitKey(1) & 0xFF == ord('q') or ret == False:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    
    obj = cascade.detectMultiScale(gray, 1.4, 3)
    

    for (x,y,w,h) in obj:
        cv.circle(frame, (x+w//2,y+h//2), h//2, (0,255,255), 2)

        
    cv.imshow('video',frame)


vid.release()
cv.destroyAllWindows()

