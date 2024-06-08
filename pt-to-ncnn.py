from ultralytics import YOLO


model = YOLO('models/epochs300_300.pt', task='detect')
model.export(format="ncnn") 