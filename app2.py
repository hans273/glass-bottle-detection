import customtkinter
from PIL import Image
from ultralytics import YOLO
import cv2




def start_detection():
    model = YOLO('./models/epochs200_192_best.pt')

    cap = cv2.VideoCapture(0)

    classNames = ['Glass Bottle', 'Plastic Bottle']

    while True:
        success, img = cap.read()
        results = model(img, stream=True)
        # Read all the bounding boxes
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # print(x1, y1, x2, y2)
                # cv2.rectangle(img, (x1, y1), (x2,y2), (255,0,255), 3)

                bbox = x1, y1, x2-x1, y2-y1
                # confidence
                conf = ceil(box.conf[0]*100)/100
                # class name
                cls = box.cls[0]

                if conf > 0.5:
                    cvzone.cornerRect(img, bbox)
                    cvzone.putTextRect(img, f'{classNames[int(cls)]} {conf}', (x1, y1 - 5),
                                    scale=0.6, thickness=1, offset=3)

    cv2.imshow('Image', img)
    cv2.waitKey(1)