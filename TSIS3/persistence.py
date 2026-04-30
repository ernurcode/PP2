import json
import os
from datetime import datetime

class Persistence:
    @staticmethod
    def load_settings():
        default_settings = {
            "sound": True,
            "car_color": "red",
            "difficulty": "normal",
            "volume": 0.7
        }
        
        if os.path.exists("settings.json"):
            try:
                with open("settings.json", "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)
                    default_settings.update(loaded_settings)
            except:
                pass
        
        return default_settings
    
    @staticmethod
    def save_settings(settings):
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    
    @staticmethod
    def load_leaderboard():
        if os.path.exists("leaderboard.json"):
            try:
                with open("leaderboard.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return []
        return []
    
    @staticmethod
    def save_leaderboard(leaderboard):
        leaderboard.sort(key=lambda x: x.get("score", 0), reverse=True)
        leaderboard = leaderboard[:10]
        
        with open("leaderboard.json", "w", encoding="utf-8") as f:
            json.dump(leaderboard, f, indent=4, ensure_ascii=False)
    
    @staticmethod
    def add_score(name, score, distance, coins):
        leaderboard = Persistence.load_leaderboard()
        
        entry = {
            "name": name,
            "score": score,
            "distance": distance,
            "coins": coins,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        leaderboard.append(entry)
        Persistence.save_leaderboard(leaderboard)