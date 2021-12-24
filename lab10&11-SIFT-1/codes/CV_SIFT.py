import numpy as np
import cv2
from matplotlib import pyplot as plt
# imgoutname = 'outputofdata5.jpg'
imgoutname = 'outputofdata3withtestpoints.jpg'
imgname1 = 'data3.jpg'
imgname2 = 'dataset/3.jpg'

sift = cv2.xfeatures2d.SIFT_create()

img1 = cv2.imread(imgname1)
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# 灰度处理图像
kp1, des1 = sift.detectAndCompute(img1,None)
# kp1是关键点(keypoints),des是描述子

img2 = cv2.imread(imgname2)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# 灰度处理图像
kp2, des2 = sift.detectAndCompute(img2,None)
# kp2是关键点(keypoints),des是描述子

# hmerge = np.hstack((gray1, gray2))
# 如果限制点数（由于特征点过多）
# img3 = cv2.drawKeypoints(img1,kp1[:20],img1,color=(255,0,255))
cv2.drawKeypoints(img1,kp1,img1,color=(255,0,255))
# 画出特征点，并显示为红色圆圈
# 如果限制点数（由于特征点过多）
# img4 = cv2.drawKeypoints(img2,kp2[:20],img2,color=(255,0,255))
cv2.drawKeypoints(img2,kp2,img2,color=(255,0,255))
#画出特征点，并显示为红色圆圈

# hmerge = np.hstack((img3, img4))

# BFMatcher匹配器
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1,des2,k=2)
# 找好的匹配
cnt = 0
newmatches = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        cnt += 1
        newmatches.append((m,n))
# img5 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches[:20],None,flags=2)
# print(len(newmatches))
print(cnt)
img5 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,newmatches,None,flags=2)
plt.imshow(img5)
plt.savefig(imgoutname)