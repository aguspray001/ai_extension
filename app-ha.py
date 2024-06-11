from ultralytics import YOLO
import cv2 as cv 
import os
from dotenv import load_dotenv
from utils import url_to_image, plotting_result, transfer_file, data_formatter
import urllib.request
import json

# Set up connection parameters
HOST = '10.0.2.28'
PORT = 8123
API_PASSWORD = 'hassio'  # Use the same password you set in configuration.yaml

# load env data
load_dotenv()
camera_entity = os.getenv('CAM_ENTITY')
token= os.getenv('HA_TOKEN')
ob_model = os.getenv('OB_MODEL') 
URI_CAM = "https://iot.hcm-lab.id/api/camera_proxy/camera.{camera_entity}?time=1462653861261".format(camera_entity=camera_entity)

# Define the data you want to send
entity_id = f'sensor.{camera_entity}'  # Replace with your custom entity ID
new_state = None  # Replace with the new state value you want to set

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

def postState(url, data):
    data = json.dumps(data)
    data = data.encode()
    print(data)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', "Authorization": "Bearer {token}".format(token=token)}, method="POST")
    resp = urllib.request.urlopen(req,  data)
    return resp
    

#read video until finish
while(1):
    #capture frame by frame
    frame = url_to_image(url=URI_CAM, token=token)
    frame = cv.resize(frame, (600, 500))
    if frame.any() == True:
        img = frame
        results = model.predict(source=frame, show=False, stream=True)
        formatedData = data_formatter(results=results)
        plotting_result(results=results, camera_entity=camera_entity)
        transfer_file(local_file_path, remote_file_path, remote_server_hostname, remote_server_port, remote_server_username, remote_server_password)
        # print(data)
        resp = postState(
                url=f"https://iot.hcm-lab.id/api/states/sensor.cctv_mahasiswa", 
                data={"state": str(camera_entity), "attributes": {"class": str(formatedData)}}
        )
        
        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

#close all frames
cv.destroyAllWindows()