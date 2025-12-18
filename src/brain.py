class TrafficBrain:
    def __init__(self, street_length_m=200, num_lanes=3):
        self.street_length = street_length_m
        self.num_lanes = num_lanes
        
        # Encombrement physique (PCE - Passenger Car Equivalent)
        self.pce_map = {
            2: 1.0,  # Voiture (~5m)
            3: 0.5,  # Moto (~2m)
            5: 2.0,  # Bus (~12m)
            7: 2.0   # Camion
        }

    def analyze_flow(self, vehicle_list):
        # 1. Calcul de l'espace total occupé (en mètres)
        # On estime qu'une unité "1.0" occupe 5m de route + 2m de distance d'arrêt
        space_occupied = sum(self.pce_map.get(vid, 1.0) * 7 for vid in vehicle_list)
        
        # 2. Capacité totale de la portion de rue (mètres cumulés des voies)
        total_road_capacity = self.street_length * self.num_lanes
        
        # 3. Calcul de l'occupation (0.0 à 1.0)
        occupancy = space_occupied / total_road_capacity if total_road_capacity > 0 else 0
        
        # 4. Calcul de la vitesse suggérée (Anti-Fantôme)
        # On utilise une décroissance linéaire : plus c'est plein, plus on ralentit tout le monde
        v_free = 80  # Vitesse max autorisée
        if occupancy > 0.9:
            suggested_speed = 10 # Presque à l'arrêt (Bouchon)
            status = "EMBOUTEILLAGE DÉTECTÉ"
        else:
            # Harmonisation de la vitesse pour éviter l'effet accordéon
            suggested_speed = v_free * (1 - occupancy)
            status = "FLUIDE" if occupancy < 0.5 else "TRAFIC DENSIFIÉ"
            
        # 5. Distance de sécurité optimale entre les voitures
        # Règle simple : (Vitesse / 3.6) * 1.5 secondes
        safe_gap = (suggested_speed / 3.6) * 1.5 if suggested_speed > 0 else 2
        
        return {
            "occupancy": round(occupancy * 100, 1),
            "speed": round(suggested_speed, 1),
            "gap": round(safe_gap, 1),
            "status": status
        }