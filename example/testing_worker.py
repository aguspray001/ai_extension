from ultralytics import YOLO
import concurrent.futures

model = YOLO('yolov8m.pt')

def worker(source_path):
    results = model(source=source_path, show=True, stream=True, imgsz=320)  # predict on an image
    # View results
    for r in results:
        print(r.boxes)  # print the Boxes object containing the detection bounding boxes

pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

pool.submit(worker('video_1.mp4'))
pool.submit(worker('video_1.mp4'))

pool.shutdown(wait=True)

print("finish")