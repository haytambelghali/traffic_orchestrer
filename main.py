import cv2
import os
from src.detector import TrafficDetector
from src.brain import TrafficBrain

def main():
    video_path = "data/test_traffic.mp4" # Remplace par ton fichier
    if not os.path.exists(video_path):
        print("Erreur : Fichier vidéo introuvable.")
        return

    cap = cv2.VideoCapture(video_path)
    detector = TrafficDetector()
    # On définit une rue de 150m avec 4 voies (comme sur ta photo)
    brain = TrafficBrain(street_length_m=150, num_lanes=4)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        # Traitement
        vehicle_ids, frame_draw = detector.get_vehicles(frame)
        data = brain.analyze_flow(vehicle_ids)

        # --- Affichage du Tableau de Bord (HUD) ---
        h, w, _ = frame_draw.shape
        cv2.rectangle(frame_draw, (0, 0), (500, 200), (0, 0, 0), -1)
        
        # Statut et Occupation
        color = (0, 0, 255) if data["occupancy"] > 80 else (0, 255, 0)
        cv2.putText(frame_draw, f"STATUS: {data['status']}", (20, 40), 2, 0.8, color, 2)
        cv2.putText(frame_draw, f"OCCUPATION: {data['occupancy']}%", (20, 80), 2, 0.8, (255, 255, 255), 1)
        
        # Vitesse suggérée pour éviter l'effet fantôme
        cv2.putText(frame_draw, f"VITESSE SUGGEREE: {data['speed']} km/h", (20, 130), 2, 0.9, (0, 255, 255), 2)
        cv2.putText(frame_draw, f"GARDER DISTANCE: {data['gap']} m", (20, 170), 2, 0.6, (200, 200, 200), 1)

        cv2.imshow("Orchestrateur de Trafic Resilient", frame_draw)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()