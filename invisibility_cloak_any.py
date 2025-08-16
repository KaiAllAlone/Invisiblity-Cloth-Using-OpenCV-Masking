import cv2 as cv 
import numpy as np
import time
import datetime


def mean_color_extractor(hsv_array):
    h_sum=0
    s_sum=0
    v_sum=0
    for i in range(0,len(hsv_array),3):
        h_sum+=hsv_array[i]
        s_sum+=hsv_array[i+1]
        v_sum+=hsv_array[i+2]
    h_mean=h_sum/(len(hsv_array)/3)
    s_mean=s_sum/(len(hsv_array)/3)
    v_mean=v_sum/(len(hsv_array)/3)
    return np.array([h_mean,s_mean,v_mean])



def capture_background():
    # Capture the background for 10 seconds
    video=cv.VideoCapture(0)
    for i in range(5):
        ret,background=video.read()
        if not ret:
            break
        background=cv.flip(background,1)
        cv.imshow("Background",background)
        time.sleep(1)
    cv.imwrite("background.jpg",background)
    video.release()
    cv.destroyAllWindows()
    

    
    
def color_extractor():
    #range of HSV colors
    hsv_array=[]
    video=cv.VideoCapture(0)
    while True:
        ret,frame=video.read()
        if not ret:
            break
        frame=cv.flip(frame,1)
        frame=cv.putText(frame,"Fill the cloth color in the ROI", (10,30),cv.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        frame=cv.rectangle(frame,(200,200),(400,400),(0,255,0),2)
        roi=frame[200:400,200:400]
        hsv_roi=cv.cvtColor(roi,cv.COLOR_BGR2HSV)
        cv.imshow("Webcam Feed",frame)
        # Calculate the mean color in the ROI
        key = cv.waitKey(1) & 0xFF
        if key == ord('s'):  # Save HSV on 's'
            hsv_mean=cv.mean(hsv_roi)[:3]
            hsv_array.append(hsv_mean)
            print('hsv mean',hsv_mean)
        elif key == ord('q'):  # Quit on 'q'
            break
    video.release()
    cv.destroyAllWindows()
    print('hsv before function return',hsv_array)
    return hsv_array




video=cv.VideoCapture(0)
#background extraction for first 10 seconds
print('Capturing background...')
capture_background()
print('Background captured. Press "q" to exit.')
print('Gathering HSV Values...,Press "s" to save the HSV values.')
hsv_array=color_extractor()
print(f"HSV Values after function: {hsv_array}")
print('HSV Values Captured. Press "q" to exit.')
hsv_cloth=np.zeros((480,640),np.uint8) #fully black
while True:
    ret,frame=video.read()
    frame=cv.flip(frame,1)
    if not ret:
        break
    hsv_image=cv.cvtColor(frame,cv.COLOR_BGR2HSV)
    background=cv.imread("background.jpg")
    hsv_cloth= np.zeros((480, 640),np.uint8)
    for arrays in hsv_array:
        h, s, v = np.array(arrays, dtype=np.uint8)
        lower = np.array([max(h-20, 0),max(s-70, 0),max(v-70, 0)],dtype=np.uint8)
        upper = np.array([min(h+20, 179),min(s+70, 255),min(v+70, 255)],dtype=np.uint8)
        color_picked = cv.inRange(hsv_image, lower, upper)
        hsv_cloth = cv.bitwise_or(hsv_cloth, color_picked)
    kernel = np.ones((3, 3), np.uint8)
    hsv_cloth = cv.morphologyEx(hsv_cloth, cv.MORPH_OPEN, kernel, iterations=2)
    hsv_cloth = cv.morphologyEx(hsv_cloth, cv.MORPH_DILATE, kernel, iterations=1)
    background_excluding_cloth=cv.bitwise_not(hsv_cloth) #this is also a mask with white portion signifying the portion in frame excluding cloth
    # Apply the mask to the background and the current frame
    background_excluding_cloth=cv.bitwise_and(frame,frame,mask=background_excluding_cloth) # only the background(live) excluding the cloth, the cloth part is black
    cloth_invisibility=cv.bitwise_and(background,background,mask=hsv_cloth) #only part of background(that was captured) where the cloth is present is seen,rest is black
    # Merge the two images
    result=cv.bitwise_or(cloth_invisibility,background_excluding_cloth)
    cv.imshow("Invisibility Cloak",result)
    if cv.waitKey(1) & 0xFF==ord('q'):
        break
cv.destroyAllWindows()
video.release()