from ultralytics import YOLO
import cv2 as cv 
import os
from dotenv import load_dotenv
from utils import url_to_image, plotting_result

# load env data
load_dotenv()
camera_entity = os.getenv('CAM_ENTITY')
token= os.getenv('HA_TOKEN')
ob_model = os.getenv('OB_MODEL') 
URI_CAM = "https://iot.hcm-lab.id/api/camera_proxy/camera.{camera_entity}?time=1462653861261".format(camera_entity=camera_entity)

# load model
model = YOLO(model="models/{ob_model}".format(ob_model=ob_model))

#read video until finish
while(1):
    #capture frame by frame
    frame = url_to_image(url=URI_CAM, token=token)
    frame = cv.resize(frame, (600, 500))
    if frame.any() == True:
        img = frame
        results = model.predict(source=frame, show=True, stream=True)
        plotting_result(results=results, camera_entity=camera_entity)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

#close all frames
cv.destroyAllWindows()