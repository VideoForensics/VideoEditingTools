import cv2
import numpy as np
import sys

def kmeans_color_quantization(image, clusters=8, rounds=1):
  h, w = image.shape[:2]
  samples = np.zeros([h*w,3], dtype=np.float32)
  count = 0
  for x in range(h):
      for y in range(w):
          samples[count] = image[x][y]
          count += 1
  compactness, labels, centers = cv2.kmeans(samples,
          clusters, 
          None,
          (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
          rounds, 
          cv2.KMEANS_RANDOM_CENTERS)
  centers = np.uint8(centers)
  res = centers[labels.flatten()]
  return res.reshape((image.shape))

def pickColors(image):
  color1 = None
  color2 = None
  qimage = kmeans_color_quantization(image, clusters=2)
  rows,cols, channels = qimage.shape
  for i in range(rows):
    for j in range(cols):
      k = qimage[i,j]
      if(type(color1) == type(None)):
        color1 = k
      elif((k != color1).all()):
        color2 = k
        return (qimage, color1, color2)
  return (qimage, color1, color2)

def applyMask(maskImgPath, ImgPath):
  image = cv2.imread(maskImgPath)
  rrImg = cv2.imread(ImgPath)
  qimage, color1,color2 = pickColors(image)
  print("color1: ", color1)
  print("color2: ", color2)
  qimage[np.where((qimage==color1).all(axis=2))] = [0,0,0]
  qimage[np.where((qimage==color2).all(axis=2))] = [255,255,255]

  im_gray = cv2.cvtColor(qimage, cv2.COLOR_BGR2GRAY)
  (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
  thresh = 127
  im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

  blurred_mask = cv2.GaussianBlur(im_bw,(11,11),0)
  maskApplied = cv2.bitwise_and(rrImg, rrImg, mask = blurred_mask)

  cv2.imshow('applied', maskApplied)
  cv2.imwrite("outputImage.png",maskApplied)

  if cv2.waitKey() == ord('q'):
      cv2.destroyAllWindows()

#applyMask('out.png','rr.jpeg')
if __name__=="__main__": 
    applyMask(sys.argv[1],sys.argv[2]) 