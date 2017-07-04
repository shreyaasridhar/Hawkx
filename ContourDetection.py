import cv2
import numpy as np

original = cv2.imread('table1.jpg')
Z = original.reshape((-1,3))
Z = np.float32(Z)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
ret,label,center=cv2.kmeans(Z,4,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((original.shape))
cv2.imshow('res2',res2)

size = res2.shape[1]

res2_gray=cv2.cvtColor( res2, cv2.COLOR_RGB2GRAY )


hist = cv2.calcHist([res2_gray],[0],None,[256],[0,256])
mi = max(hist)
for i in range(len(hist)):
    if(hist[i]==mi):
        break
print i

mask = np.array(res2_gray)
mask[res2_gray==i]=0

output = cv2.bitwise_and(res2, res2, mask = mask)


gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
i=0
contours = sorted(contours, key = lambda x:cv2.contourArea(x),reverse=True)
for j in contours:
    if i>20:
        break
    x,y,w,h = cv2.boundingRect(j)
    cv2.rectangle(gray,(x-5,y-5),(x+w+10,y+h+10),(0,255,0),2)
    i=i+1
cv2.imshow('image',gray)

cv2.waitKey(0)
