from ultralytics import YOLO

model = YOLO("runs/detect/train4/weights/best.pt")

model.train(data=r"C:\Users\namwe\PycharmProjects\YOLOVisualise\FruitsDataset-refactored\data.yaml", epochs=30)
