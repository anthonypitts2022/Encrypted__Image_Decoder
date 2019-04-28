"""
Author: Anthony Pitts
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math

# this makes image look better on a macbook pro
def imageshow(img, dpi=200):
    if dpi > 0:
        F = plt.gcf()
        F.set_dpi(dpi)
    plt.imshow(img)
    
    
#this removes all rgb color other than pgb specified
def onechannel(pattern,pgb):
    red,green,blue = range(3)
    #reads image as plt
    im = plt.imread(pattern)
    shape = im.shape
    #iterates over width
    for x in range(shape[0]):
        #iterates over height
        for y in range(shape[1]):
            #if only want red colors in image
            if pgb==red:
                #remove blue colors
                if im[x,y,blue] != 0:
                    im[x,y,blue] = 0
                #remove green colors
                if im[x,y,green] != 0:
                    im[x,y,green] = 0
            #if only want green colors in image
            if pgb==green:
                #remove blue colors
                if im[x,y,blue] != 0:
                    im[x,y,blue] = 0
                #remove red colors
                if im[x,y,red] != 0:
                    im[x,y,red] = 0
            #if only want blue colors in image
            if pgb==blue:
                #remove green colors
                if im[x,y,green] != 0:
                    im[x,y,green] = 0
                #remove red colors
                if im[x,y,red] != 0:
                    im[x,y,red] = 0
    return im

#takes in size 3 list [red,green,blue] that declares how to permute colors in image
#i.e. perm= [1,1,2] makes all red (nomrally 0), green (1)
def permutecolorchannels(img, perm): 
    swap_red_with = perm[0]
    swap_green_with = perm[1]
    swap_blue_with = perm[2]
    red,green,blue = range(3)
    #read in image
    im = plt.imread(img)
    im_copy = im.copy()
    shape = im.shape
    #iterates over width
    for x in range(shape[0]):
        #iterates over height
        for y in range(shape[1]):
            #amount/weight of each color (from 0-255)
            amt_red = im[x,y,red]
            amt_green = im[x,y,green]
            amt_blue = im[x,y,blue]
            #if current pixel is red
            if im[x,y,red] != 0:
                #if red should be swapped with another color
                if swap_red_with!=0:
                    #swap with green
                    if swap_red_with == 1:
                        im_copy[x,y,red] = amt_green
                        im_copy[x,y,green] = amt_red
                    #swap with blue
                    if swap_red_with == 2:
                        im_copy[x,y,blue] = amt_red
                        im_copy[x,y,red] = amt_blue
            #if current pixel is green
            if im[x,y,green] != 0:
                #if green should be swapped with another color
                if swap_green_with!=1:
                    #swap with red
                    if swap_green_with == 0:
                        im_copy[x,y,green] = amt_red
                        im_copy[x,y,red] = amt_green
                    #swap with blue
                    if swap_green_with == 2:
                        im_copy[x,y,green] = amt_blue
                        im_copy[x,y,blue] = amt_green
            #if current pixel is blue
            if im[x,y,blue] != 0:
                #if blue should be swapped with another color
                if swap_blue_with!=2:
                    #swap with red
                    if swap_blue_with == 0:
                        im_copy[x,y,blue] = amt_red
                        im_copy[x,y,red] = amt_blue
                    #swap with blue
                    if swap_blue_with == 1:
                        im_copy[x,y,green] = amt_blue
                        im_copy[x,y,blue] = amt_green
    return im_copy

#decrypts image using XOR key technique
def decrypt(image, key):
    r = 0 #red index
    g = 1 #green index
    b = 2 #blue index
    im = image
    shape = im.shape
    decrypted_img = np.zeros(shape, dtype=im.dtype)
    #iterates over width
    for x in range(shape[0]):
        #iterates over height
        for y in range(shape[1]):
            #uses the XOR key on the red, green, and blue components of each pixel
            red = im[x,y,r]^key[y]
            green = im[x,y,g]^key[y]
            blue = im[x,y,b]^key[y]
            #adds the new red, green, blue values to the decrypted image
            decrypted_img[x,y,:] = (red,green,blue)
    return decrypted_img      
            
            
        
def __main__():
    pattern = 'pattern.png'
    imageshow(plt.imread(pattern))
    plt.imshow(onechannel(pattern,2))
    plt.imshow(permutecolorchannels(pattern, [2,0,1]))
    imageshow(plt.imread('permcolors.jpg'))
    plt.imshow(permutecolorchannels('permcolors.jpg', [1,2,0]))
    secret = plt.imread('secret.bmp')
    key = np.load('key.npy')
    plt.imshow(decrypt(secret,key))
    
__main__()
