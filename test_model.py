from ultralytics import YOLO

model = YOLO("runs/detect/train4/weights/best.pt")

model.val()
# model.predict(0, show=True)
