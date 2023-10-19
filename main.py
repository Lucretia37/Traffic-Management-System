import cv2
import video
# cap=cv2.VideoCapture(0)
# cap=cv2.VideoCapture("sample9.mp4")
cap=cv2.VideoCapture("sample3.mp4")
while True:
    ret,frame=cap.read()
    rescale_frame=cv2.resize(frame, (0, 0), None, 0.70, 0.70)
    gray_frame= cv2.cvtColor(rescale_frame, cv2.COLOR_BGR2RGB)
    if ret == True:
        predictions=video.interference(rescale_frame)
        video.plate(predictions,rescale_frame)

        # video.plate(predictions,frame)
    else:
        break
