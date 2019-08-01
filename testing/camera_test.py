import cv2
cam1 = cv2.VideoCapture(0) # This is your first video camera at index'zero'
s, img = cam1.read()
picName = 'pic.png'
cv2.imwrite(picName, img)
