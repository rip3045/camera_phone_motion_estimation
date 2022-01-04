# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2 
import numpy as np
import time

img = cv2.imread("red_panda.jpg", 0)
print(img.shape)

##create the dectecor objects

#sift = cv2.xfeatures2d.SIFT_create()
#surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create(nfeatures=500)
tic = time.time()
#keypoints_sift, descriptors = sift.detectAndCompute(img, None)
#keypoints_surf, descriptors = surf.detectAndCompute(img, None)
keypoints_orb, descriptors = orb.detectAndCompute(img, None)
toc = time.time()

print(toc-tic)
print(len(keypoints_orb))

img1 = cv2.drawKeypoints(img, keypoints_orb, None)
#cv2.imwrite("output/orb_out3.jpg", img1)

#img2 = cv2.drawKeypoints(img, keypoints_sift, None)
#cv2.imwrite("output/sift_out3.jpg", img2)

#img3 = cv2.drawKeypoints(img, keypoints_surf, None)
#cv2.imwrite("output/surf_out3.jpg", img3)


##cv2.imshow("Image", img)
##cv2.waitKey(0)
##cv2.destroyAllWindows()