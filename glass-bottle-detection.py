import numpy as np
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *

# Video files-
file = 'assets/sanmig2.mp4'
cap = cv2.VideoCapture(0)

model = YOLO('models/epochs300_170.pt', task='detect')
model.export(format="ncnn") 

classNames = ['Glass Bottle', 'Plastic Bottle']

tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.5)

tracked_ids = set()
bottle_count = 0
ncnn_model = YOLO("models/epochs300_170_ncnn_model", task="detect")

while True:
    success, img = cap.read()
    results = ncnn_model(img, stream=True)
    detections = np.empty((0, 5))

    # Read all the bounding boxes
    for r in results:
        boxes = r.boxes
        tmp_max = 0
        detection = []
        for box in boxes:
            print('BOXXX: ', box)
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # print(x1, y1, x2, y2)
            # cv2.rectangle(img, (x1, y1), (x2,y2), (255,0,255), 3)

            bbox = x1, y1, x2-x1, y2-y1
            # confidence
            conf = math.ceil(box.conf[0]*100)/100
            # class name
            cls = box.cls[0]

            if conf > 0.7 and cls == 0:
                cur_array = np.array([x1, y1, x2, y2, conf])
                if conf > tmp_max:
                    tmp_max = conf
                    detection = cur_array
    if len(detection):
        detections = np.vstack((detections, cur_array))
        
    tracker_res = tracker.update(detections)

    for result in tracker_res:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
        bbox = x1, y1, x2 - x1, y2 - y1
        cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), thickness=2)
        cv2.rectangle(img, (x1,y1-70), (x1+200,y1), (0,255,0), thickness=-1)
        cv2.putText(img, f'{int(id)} {tmp_max}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), thickness=5, lineType=cv2.LINE_8)
        if id not in tracked_ids:
            bottle_count += 1
            tracked_ids.add(id)

    cvzone.putTextRect(img, f'Glass Bottles: {bottle_count}', (10, 50))
    cv2.imshow('Image', img)
    cv2.waitKey(1)