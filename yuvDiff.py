from PIL import Image
import numpy as np
import cv2


def PIL2array(img,channel):
    return np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], channel)


#This function will overlay a grid on the input image
def overlayGrid(img,width,height,blocksize):
    for i in range(height):
        for j in range(0,(width),blocksize):
            img[:,:,1][i][j]=0
            img[:,:,1][i][j+1]=0
            img[:,:,2][i][j]=0
            img[:,:,2][i][j+1]=0
    
    for i in range(0,height,blocksize):
        for j in range(width):
            img[:,:,1][i][j]=0
            img[:,:,1][i+1][j]=0
            img[:,:,2][i][j]=0
            img[:,:,2][i+1][j]=0
    return img

width=352
height=288
blocksize=64

imgmod=np.zeros(shape=(height,width,3),dtype='uint8')

try:
    #process refrence image
    fref = open("coastguard_352x288_P420.yuv", "rb")
    fmod = open("coastguard_352x288_P420_mod.yuv", "rb")
    imgref=np.zeros(shape=(height,width,3),dtype='uint8')
    imgmod=np.zeros(shape=(height,width,3),dtype='uint8')
    byteref = fref.read(width*height)
    bytemod = fmod.read(width*height)
    PILimgref=Image.frombytes("P",(width,height),byteref,decoder_name='raw')
    PILimgmod=Image.frombytes("P",(width,height),bytemod,decoder_name='raw')
    cvimgref=PIL2array(PILimgref,1)
    cvimgmod=PIL2array(PILimgmod,1)
    imgref[:,:,0]=cvimgref[:,:,0]
    imgmod[:,:,0]=cvimgmod[:,:,0]
    imgref[:,:,1]=cvimgref[:,:,0]
    imgmod[:,:,1]=cvimgmod[:,:,0]
    imgref[:,:,2]=cvimgref[:,:,0]
    imgmod[:,:,2]=cvimgmod[:,:,0]

    overlayedimg=overlayGrid(imgref,width,height,blocksize)
    
    
    cv2.imshow("s",overlayedimg)
    cv2.waitKey(0)
finally:
    fref.close()
    
    
    
#1 (1-bit pixels, black and white, stored with one pixel per byte)
#L (8-bit pixels, black and white)
#P (8-bit pixels, mapped to any other mode using a color palette)
#RGB (3x8-bit pixels, true color)
#RGBA (4x8-bit pixels, true color with transparency mask)
#CMYK (4x8-bit pixels, color separation)
#YCbCr (3x8-bit pixels, color video format)
#Note that this refers to the JPEG, and not the ITU-R BT.2020, standard
#LAB (3x8-bit pixels, the L*a*b color space)
#HSV (3x8-bit pixels, Hue, Saturation, Value color space)
#I (32-bit signed integer pixels)
#F (32-bit floating point pixels)