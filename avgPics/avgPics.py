import cv2
import numpy as np
import sys

def readFile(inputpath):
    return cv2.imread(inputpath)

def subtractBg(fgPic, bgPic):
    #img = fgPic - bgPic
    frame_diff = cv2.absdiff(fgPic, bgPic)
    gray_diff = cv2.cvtColor(frame_diff, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(gray_diff, 10, 255)
    res = cv2.bitwise_and(fgPic,fgPic, mask= mask)
    return res, mask

def addPhotos(arrPhotos):
    dst = np.zeros(arrPhotos[0].shape,np.uint8)
    for i in range(len(arrPhotos)):
        dst = cv2.add(arrPhotos[i],dst)
    return dst

def addJustDiff(arrPhotos):
    dst = np.zeros(arrPhotos[0].shape,np.uint8)
    for i in range(len(arrPhotos)):
        diff = cv2.absdiff(arrPhotos[i], dst)
        dst = cv2.add(diff,dst)
    return dst

def addPhotosWithMask(arrPhotos, bg,bUseMask=True):
    dst = bg.copy()
    for i in range(len(arrPhotos)):
        sub, mask = subtractBg(arrPhotos[i], bg)
        cv2.imwrite("mask.png",mask)
        if(bUseMask):
            maskBGR = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            dst = cv2.subtract(dst,maskBGR)
        dst = cv2.add(sub,dst)
    return dst
    

def MakeGhost(bg, fgArr):
    dst = addPhotosWithMask(fgArr, bg, False)
    cv2.imshow('result',dst)
    while(True):
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
    cv2.imwrite("ghost.png",dst)


if __name__=="__main__": 
    bg = readFile(sys.argv[1])
    fgArr = list(map(readFile, sys.argv[1:]))
    MakeGhost(bg,fgArr)