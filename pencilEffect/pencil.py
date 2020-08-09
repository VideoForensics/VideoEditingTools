import cv2
import numpy as np
import sys

def pencil(imgPath):
    img = cv2.imread(imgPath)
    dst,mask = cv2.pencilSketch(img,sigma_s=20,sigma_r=.4,shade_factor=.02)
    cv2.imshow('result',dst)
    cv2.imshow('mask',mask)
    while(True):
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()

if __name__=="__main__": 
    pencil(sys.argv[1])