from ultralytics import YOLO
import cv2 as cv 
import os
from dotenv import load_dotenv
from utils import url_to_image, plotting_result, transfer_file

# load env data
load_dotenv()
camera_entity = os.getenv('CAM_ENTITY')
token= os.getenv('HA_TOKEN')
ob_model = os.getenv('OB_MODEL') 
URI_CAM = "https://iot.hcm-lab.id/api/camera_proxy/camera.{camera_entity}?time=1462653861261".format(camera_entity=camera_entity)

# load model
model = YOLO(model="models/{ob_model}".format(ob_model=ob_model))

# sftp
# Replace these values with your own
local_file_path = 'results/cctv_ruang_mahasiswa_y8_latest.jpg'
remote_file_path = "/root/config/www/cctv_ruang_mahasiswa_y8_latest.jpg"
remote_server_hostname = '10.0.2.28'
remote_server_port = 22  # Default SSH port
remote_server_username = 'root'
remote_server_password = 'hassio'

#read video until finish
while(1):
    #capture frame by frame
    frame = url_to_image(url=URI_CAM, token=token)
    frame = cv.resize(frame, (600, 500))
    if frame.any() == True:
        img = frame
        results = model.predict(source=frame, show=True, stream=True)
        plotting_result(results=results, camera_entity=camera_entity)
        transfer_file(local_file_path, remote_file_path, remote_server_hostname, remote_server_port, remote_server_username, remote_server_password)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

#close all frames
cv.destroyAllWindows()