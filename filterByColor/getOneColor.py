import cv2
import numpy as np
import sys
import time
import click


refPt = []
cropping = False

def click_and_crop(event, x, y, flags, param):
	# grab references to the global variables
	global refPt, cropping
 
	# if the left mouse button was clicked, record the starting
	# (x, y) coordinates and indicate that cropping is being
	# performed
	if event == cv2.EVENT_LBUTTONDOWN:
		refPt = [(x, y)]
		cropping = True
 
	# check to see if the left mouse button was released
	elif event == cv2.EVENT_LBUTTONUP:
		# record the ending (x, y) coordinates and indicate that
		# the cropping operation is finished
		refPt.append((x, y))
		cropping = False

def findHSVOfBoundingBoxVideo(videopath):
    vidcap = cv2.VideoCapture(videopath)
    #property_id = int(cv2.CAP_PROP_FRAME_COUNT) 
    #length = int(cv2.VideoCapture.get(vidcap, property_id))
    return findHSVOfBoundingBox(vidcap,-1)

def findHSVOfBoundingBoxCam():
    vidcap = cv2.VideoCapture(0)
    # allow the camera or video file to warm up
    vidcap.read()
    time.sleep(2.0)
    return findHSVOfBoundingBox(vidcap,50)

def findHSVOfBoundingBox(vidcap, quitAfterNFrames):
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", click_and_crop)
    success = True
    hMin = sys.maxsize
    sMin = sys.maxsize
    vMin = sys.maxsize
    minint = -sys.maxsize - 1
    hMax = minint
    sMax = minint
    vMax = minint
    frameCount = 0
    while(success):
        success,frame = vidcap.read()
        if(not success):
            break
        focus = None
        focushsv = None
        cv2.imshow('frame',frame)
        while(True):

            if(len(refPt)> 1 and abs(refPt[0][0]-refPt[1][0]) > 0 
                and abs(refPt[0][1]-refPt[1][1]) > 0 ):
                cv2.rectangle(frame, refPt[0], refPt[1], (0, 255, 0), 2)
                focus = frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
                focushsv = cv2.cvtColor(focus, cv2.COLOR_BGR2HSV)
                rows,cols, channels = focushsv.shape
                break
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        cv2.imshow('frame',frame)
        if(len(refPt)> 1):
            cv2.imshow('focus',focus)
            cv2.imshow('focushsv',focushsv)
            for i in range(rows):
                for j in range(cols):
                    curH = focushsv[i,j][0]
                    curS = focushsv[i,j][1]
                    curV = focushsv[i,j][2]
                    #print "curr hsv = h: {}, s: {}, v: {}".format(curH,curS,curV)
                    if(hMin > curH):
                        hMin = curH
                    if(sMin > curS):
                        sMin = curS
                    if(vMin > curV):
                        vMin = curV

                    if(hMax < curH):
                        hMax = curH
                    if(sMax < curS):
                        sMax = curS
                    if(vMax < curV):
                        vMax = curV
        frameCount = frameCount +1
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
        if(quitAfterNFrames is not -1 and quitAfterNFrames is frameCount):
            break
    print("Max hsv = h: {}, s: {}, v: {}".format(hMax,sMax,vMax))
    print("Min hsv = h: {}, s: {}, v: {}".format(hMin,sMin,vMin))
    cv2.destroyAllWindows()
    vidcap.release()
    return ([hMax,sMax,vMax],[hMin,sMin,vMin])

def testColorChoice(vidcap,lowerBound,upperBound):
    success = True
    kernel = np.ones((5,5),np.uint8)
    while(success):
        success,frame = vidcap.read()
        if(not success):
            break
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_color = np.array(lowerBound)
        upper_color = np.array(upperBound)

        mask = cv2.inRange(hsv, lower_color, upper_color)
        res = cv2.bitwise_and(frame,frame, mask= mask)
        dilate = cv2.dilate(res,kernel,iterations = 1)
        #cv2.imshow('frame',frame)
        #cv2.imshow('mask',mask)
        #cv2.imshow('res',res)
        cv2.imshow('dilate',dilate)

        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break

    cv2.destroyAllWindows()
    vidcap.release()

def testColorChoiceVideo(videopath,lowerBound,upperBound):
    vidcap = cv2.VideoCapture(videopath)
    testColorChoice(vidcap,lowerBound,upperBound)

def testColorChoiceCam(lowerBound,upperBound):
    vidcap = cv2.VideoCapture(0)
    testColorChoice(vidcap,lowerBound,upperBound)

import click

#makeVideo(applyEffects("buffercapture.mp4",[flipHorizontal,flipColorChannels]),"flip2")
@click.command()
@click.option('-i', '--input', help='input name')
def options(input):
    if(input != None and input != ''):
        testValues = findHSVOfBoundingBoxVideo(input)
        testColorChoiceVideo(input,testValues[1],testValues[0])
    else:
        testValues = findHSVOfBoundingBoxCam()
        testColorChoiceCam(testValues[1],testValues[0])

if __name__ == '__main__':
    options()
