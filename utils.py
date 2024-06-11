import numpy as np
import urllib.request
import cv2
from PIL import Image
from ultralytics.utils.plotting import Annotator
import paramiko
import os
  
def url_to_image(url, token):
	# download the image, convert it to a NumPy array, and then read
	# it into OpenCV format
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', "Authorization": "Bearer {token}".format(token=token)})
    resp = urllib.request.urlopen(req)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
	# return the image
    return image
    
def plotting_result(results, camera_entity):
    # Show the results
    image_path="results"
    for r in results:
        im_array = r.plot()  # plot a BGR numpy array of predictions
        im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        im.save(f"{image_path}"+"/{camera_entity}_y8_latest.jpg".format(camera_entity=camera_entity))  # save image
        

def transfer_file(local_path, remote_path, hostname, port, username, password):
    
    local_abs_path = os.path.abspath(local_path)
    # Create an SSH client
    ssh = paramiko.SSHClient()

    try:
        # Automatically add the server's host key
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server
        ssh.connect(hostname, port, username, password)

        # Open an SFTP session on the SSH connection
        sftp = ssh.open_sftp()

        # Upload the local file to the remote server
        sftp.put(local_path, remote_path)

        print(f"File {local_abs_path} transferred to {remote_path} successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the SFTP session and the SSH connection
        if sftp:
            sftp.close()
        if ssh:
            ssh.close()