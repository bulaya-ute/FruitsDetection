from ultralytics import YOLO

model = YOLO()

model.train(data=r"C:\Users\Bulaya\Desktop\fruits\YOLODataset\dataset.yaml", epochs=30)
