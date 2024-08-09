from ultralytics import YOLO

# model = YOLO("runs/detect/train4/weights/best.pt")
model = YOLO("yolov8n-seg.pt")

# model.val()
model.predict(0, show=True)
