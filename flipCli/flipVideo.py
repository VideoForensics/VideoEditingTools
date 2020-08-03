import cv2
import numpy as np
import click

#makeVideo(applyEffects("buffercapture.mp4",[flipHorizontal,flipColorChannels]),"flip2")
@click.command()
@click.option('-v', '--vertical', default=False, is_flag=True, help='flips the image veritcally')
@click.option('-h', '--horizontal', default=False, is_flag=True, help='flips the image horizontally')
@click.option('-c', '--color', default=False, is_flag=True, help='flips the r and b color channels')
@click.option('-o', '--output', default='out', help='output name')
@click.option('-i', '--input', help='input name')
def options(vertical, horizontal, color,output,input):
    effectsArr = []
    if(vertical and horizontal):
        effectsArr.append(flipBoth)
    elif vertical :
         effectsArr.append(flipVertical)
    elif horizontal :
         effectsArr.append(flipHorizontal)
    print("color is: ",color)
    if color:
         effectsArr.append(flipColorChannels)
    print("effects added: ", len(effectsArr))
    makeVideo(applyEffects(input,effectsArr),output)


def makeVideo(inputArr,outputFileName):
    width, height, channels = inputArr[0].shape
    #width, height = inputArr[:2].shape
    print("height: {} width: {}".format(height,width))
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')  # 'x264' doesn't work
    out = cv2.VideoWriter('{}.mp4'.format(outputFileName), fourcc, 29.0, (height,width))
    for img in inputArr:
        out.write(img)
    out.release()

def flipHorizontal(image):
    return cv2.flip(image, 0 )

def flipVertical(image):
    return cv2.flip(image, 1 )

def flipBoth(image):
    return cv2.flip(image, -1 )

def flipColorChannels(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def applyEffects(videopath, effectsArr):
    vidcap = cv2.VideoCapture(videopath)
    success,image = vidcap.read()
    success = True
    outputArr = []
    while success:
        for effect in effectsArr:
            image = effect(image)
        outputArr.append(image.copy())
        success,image = vidcap.read()
    print("# of frames: {}".format(len(outputArr)))
    return outputArr

if __name__ == '__main__':
    options()