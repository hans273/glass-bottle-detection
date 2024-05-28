import numpy as np
from ultralytics import YOLO
import cv2
import cvzone
import math
from sort import *
from threading import *

import customtkinter
from PIL import Image
from print_gooj import print_receipt_func 



customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("1024x600")

large_bottle_image = Image.open('./images/large-bottle.png')
small_bottle_image = Image.open('./images/small-bottle.png')


out_rel = {'relx_out': 2, 'rely_out': 2}
start_button = {'relx': 0.5, 'rely': 0.5}
stop_button = {'relx': 0.65, 'rely': 0.5}
continue_pos = {'relx': 0.15, 'rely': 0.5}
print_pos = {'relx': 0.60, 'rely': 0.5}
small_bottle_pos = {'relx': 0.157, 'rely': 0.7}
large_bottle_pos = {'relx': 0.417, 'rely': 0.7}

small_bottle_image_pos = {'relx': 0.05, 'rely': 0.3}
large_bottle_image_pos = {'relx': 0.3, 'rely': 0.2}

large_bottle_counter = [0]
small_bottle_counter = [0]

tracked_ids = set()
bottle_count = [0]
scanning = [True]

def scanner():
    cap = cv2.VideoCapture(0)
    global scanning

    model = YOLO('models/epochs300_170.pt', task='detect')
    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.5)

    ncnn_model = YOLO("models/epochs300_170_ncnn_model")
    
    if not scanning[0]:
        cap.release()
        cv2.destroyAllWindows()

    while scanning[0]:
        success, img = cap.read()

        # AI MODEL
        results = ncnn_model(img)

        detections = np.empty((0, 5))

        

        for r in results:
            boxes = r.boxes
            tmp_max = 0
            detection = []
            for box in boxes:
                
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                # confidence
                conf = math.ceil(box.conf[0]*100)/100
                # class id, glass = 0, plastic = 1
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
                # cv2.rectangle(img, (x1,y1-70), (x1+200,y1), (0,255,0), thickness=-1)
                # cv2.putText(img, f'{int(id)} {tmp_max}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), thickness=5, lineType=cv2.LINE_8)
                cvzone.putTextRect(img, f'{int(id)} {tmp_max}', (x1, y1 - 10))
                print("RESULTS: ", detections)
                if id not in tracked_ids:
                    tracked_ids.add(id)
                    bottle_count[0] += 1
                    height = y2-y1
                    if height <= 350:
                        small_bottle_counter[0] += 1
                        small_bottle_count.configure(text=f"Small Bottle \n {small_bottle_counter[0]}")
                    else:
                        large_bottle_counter[0] += 1
                        large_bottle_count.configure(text=f"Large Bottle \n {large_bottle_counter[0]}")
            
            cvzone.putTextRect(img, f'Glass Bottles: {bottle_count[0]}', (10, 50))
            cv2.imshow('Image', img)
            cv2.waitKey(1)
    
   

thread1 = Thread(target=scanner) 

def start_scan():
    print("button pressed")
    start.place(anchor=customtkinter.CENTER, relx=out_rel['relx_out'], rely=out_rel['rely_out'])
    stop.place(relx=stop_button['relx'], rely=stop_button['rely'])
    large_bottle_count.place(relx=large_bottle_pos['relx'], rely=large_bottle_pos['rely'])
    small_bottle_count.place(relx=small_bottle_pos['relx'], rely=small_bottle_pos['rely'])
    image_large_label.configure(font=("Segoe UI Semibold", 32))
    image_large_label.place(relx=large_bottle_image_pos['relx'], rely=large_bottle_image_pos['rely'])
    image_small_label.place(relx=small_bottle_image_pos['relx'], rely=small_bottle_image_pos['rely'])
    thread1 = Thread(target=scanner)
    thread1.start() 

def stop_scan():
    print("button 2 pressed")
    # button.place(anchor=customtkinter.CENTER, relx=start_button['relx'], rely=start_button['rely'])
    stop.place(relx=out_rel['relx_out'], rely=out_rel['relx_out'])
    large_bottle_count.place(relx=out_rel['relx_out'], rely=out_rel['relx_out'])
    small_bottle_count.place(relx=out_rel['relx_out'], rely=out_rel['relx_out'])
    continue_button.place(relx=continue_pos['relx'], rely=continue_pos['rely'])
    print_button.place(relx=print_pos['relx'], rely=print_pos['rely'])

    image_large_label.place(relx=out_rel['relx_out'], rely=out_rel['relx_out'])
    image_small_label.place(relx=out_rel['relx_out'], rely=out_rel['relx_out'])
    scanning[0] = False
    thread1.join()
    

def print_receipt():
    print("print button")
    start.place(anchor=customtkinter.CENTER, relx=start_button['relx'], rely=start_button['rely'])
    continue_button.place(relx=out_rel['relx_out'], rely=out_rel['rely_out'])
    print_button.place(relx=out_rel['relx_out'], rely=out_rel['rely_out'])
    scanning[0] = False
    print_receipt_func(large_bottle_counter[0], small_bottle_counter[0])


def continue_scan():
    print("continue button pressed")
    # button.place(anchor=customtkinter.CENTER, relx=out_rel['relx_out'], rely=out_rel['rely_out'])
    stop.place(relx=stop_button['relx'], rely=stop_button['rely'])

    large_bottle_count.place(relx=large_bottle_pos['relx'], rely=large_bottle_pos['rely'])
    small_bottle_count.place(relx=small_bottle_pos['relx'], rely=small_bottle_pos['rely'])

    continue_button.place(relx=out_rel['relx_out'], rely=out_rel['rely_out'])
    print_button.place(relx=out_rel['relx_out'], rely=out_rel['rely_out'])

    image_large_label.place(relx=large_bottle_image_pos['relx'], rely=large_bottle_image_pos['rely'])
    image_small_label.place(relx=small_bottle_image_pos['relx'], rely=small_bottle_image_pos['rely'])
    scanning[0] = True
    thread1 = Thread(target=scanner)
    thread1.start()


# Use CTkButton instead of tkinter Button

image_large_bottle = customtkinter.CTkImage(dark_image=large_bottle_image, size=(290,340))
image_small_bottle = customtkinter.CTkImage(dark_image=small_bottle_image, size=(290,265))
image_large_label = customtkinter.CTkLabel(master=app, text="", font=("Segoe UI Semibold",64), fg_color="transparent", image=image_large_bottle)
image_small_label = customtkinter.CTkLabel(master=app, text="", width=290, height=100, font=("Segoe UI Semibold",64), fg_color="transparent", image=image_small_bottle)

start = customtkinter.CTkButton(master=app, text="Start Scan", width=300, height=80, corner_radius=12, font=("Segoe UI Semibold",24), command=start_scan)
start.place(anchor=customtkinter.CENTER, relx=start_button['relx'], rely=start_button['rely'])

stop = customtkinter.CTkButton(master=app, text="Stop Scan", width=300, height=80, corner_radius=12, font=("Segoe UI Semibold",24), command=stop_scan)
stop.place(relx=out_rel['relx_out'], rely=out_rel['rely_out'])

continue_button = customtkinter.CTkButton(master=app, width=300, height=80, corner_radius=12, font=("Segoe UI Semibold",24), text="Continue Scan", command=continue_scan)

print_button = customtkinter.CTkButton(master=app, width=300, height=80, corner_radius=12, font=("Segoe UI Semibold",24), text="Print Receipt", command=print_receipt)
continue_button.place(relx=out_rel['relx_out'], rely=out_rel['rely_out'])
print_button.place(relx=out_rel['relx_out'], rely=out_rel['rely_out'])




large_bottle_count = customtkinter.CTkLabel(master=app, text=f"Large Bottle \n {large_bottle_counter[0]}")
small_bottle_count = customtkinter.CTkLabel(master=app, text=f"Small Bottle \n {small_bottle_counter[0]}")

large_bottle_count.place(relx=out_rel['relx_out'], rely=out_rel['relx_out'])
small_bottle_count.place(relx=out_rel['relx_out'], rely=out_rel['relx_out'])



image_large_label.place(relx=out_rel['relx_out'], rely=out_rel['relx_out'])
image_large_label.place(relx=out_rel['relx_out'], rely=out_rel['relx_out'])


app.mainloop()


