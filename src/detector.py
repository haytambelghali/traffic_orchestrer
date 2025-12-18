from ultralytics import YOLO
import cv2

class TrafficDetector:
    def __init__(self):
        # Utilisation du modèle Nano (rapide). 
        # Si la détection reste faible, tu pourras tester 'yolov8s.pt'
        self.model = YOLO('yolov8n.pt')
        # IDs COCO : 2: car, 3: motorcycle, 5: bus, 7: truck
        self.target_ids = [2, 3, 5, 7]

    def get_vehicles(self, frame):
        # conf=0.15 : très sensible pour capter les voitures vues d'en haut
        # imgsz=640 : force la résolution d'analyse
        results = self.model(frame, classes=self.target_ids, conf=0.15, imgsz=640, verbose=False)
        
        # Liste des classes détectées
        labels = [int(box.cls) for box in results[0].boxes]
        # Image avec les boîtes tracées
        annotated_img = results[0].plot()
        
        return labels, annotated_img