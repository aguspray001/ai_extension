from ultralytics import YOLO
import cv2 as cv 

# URI_CAM = 'rtsp://admin:l4bhcmlt9@192.168.9.250:8554/Streaming/Channels/102'
# URI_CAM = 'rtsp://admin:adminsds1@172.16.112.137/Streaming/Channels/101'
# URI_CAM = 'rtsp://admin:Adminsds1@172.16.112.137/Streaming/Channels/101'
URI_CAM = 'rtsp://192.168.9.20:8554/live'
# URI_CAM = 'rtsp://admin:Hiksds123@172.16.112.103:554/Streaming/Channels/101'
cap = cv.VideoCapture(URI_CAM)
model = YOLO('yolov8m.pt')

#check camera is opened successfully
if(cap.isOpened() == False):
    print("Error opening camera")

#read video until finish
while(cap.isOpened()):
    #capture frame by frame
    ret, frame = cap.read()
    frame = cv.resize(frame, (600, 500))
    if ret == True:
        img = frame
        
        results = model.predict(source=frame, show=True, stream=True, classes=[0,3,4,6,8])
        for r in results:
            print(r.boxes)
            #press Q to logout
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

#release video capture object
cap.release()
#close all frames
cv.destroyAllWindows()

# model = YOLO('yolov8m.pt')

# results = model(source='video_2.mp4', show=True, stream=True, imgsz=320)  # predict on an image
# # View results
# for r in results:
#     print(r.boxes)  # print the Boxes object containing the detection bounding boxes