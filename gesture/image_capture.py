import cv2

videoCaptureObject = cv2.VideoCapture(0)
i=1
result = True
while(result):
    ret,frame = videoCaptureObject.read()
    i=i+1
    if i > 3:
        cv2.imwrite("NewPicture.jpg", frame)
        result = False


videoCaptureObject.release()
cv2.destroyAllWindows()

