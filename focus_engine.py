import datetime
import json
import os

class FocusEngine:
    def __init__(self, storage_file="focus_data.json"):
        self.storage_file = storage_file
        self.total_focus_minutes = 0
        self.study_streak = 0
        self.xp = 0
        self.sessions_log = []
        self.load_data()

    def log_focus_session(self, module_code, duration_minutes, notes=""):
        duration = int(duration_minutes)
        xp_earned = duration * 10
        
        session_entry = {
            "module": module_code.upper(),
            "duration": duration,
            "xp_earned": xp_earned,
            "notes": notes,
            "date": str(datetime.date.today())
        }
        
        self.sessions_log.append(session_entry)
        self.total_focus_minutes += duration
        self.xp += xp_earned
        self.study_streak += 1
        
        self.save_data()
        print(f"[+] Focus Sprint Completed! [{module_code}] - {duration} mins logged.")
        print(f"    +{xp_earned} XP Earned! Total XP: {self.xp} | Current Streak: {self.study_streak} sessions")

    def get_focus_stats(self):
        hours = self.total_focus_minutes // 60
        minutes = self.total_focus_minutes % 60
        return {
            "total_time": f"{hours}h {minutes}m",
            "total_xp": self.xp,
            "streak": self.study_streak,
            "total_sessions": len(self.sessions_log)
        }

    def save_data(self):
        data = {
            "total_focus_minutes": self.total_focus_minutes,
            "study_streak": self.study_streak,
            "xp": self.xp,
            "sessions_log": self.sessions_log
        }
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    data = json.load(f)
                    self.total_focus_minutes = data.get("total_focus_minutes", 0)
                    self.study_streak = data.get("study_streak", 0)
                    self.xp = data.get("xp", 0)
                    self.sessions_log = data.get("sessions_log", [])
            except Exception as e:
                print(f"[!] Error loading focus data: {e}")

if __name__ == "__main__":
    print("=== STUDENT OS: MENTAL & FOCUS ENGINE ===")
    
    tracker = FocusEngine()
    
    tracker.log_focus_session("PRG1501", 25, "Practicing Java array scope and private methods.")
    tracker.log_focus_session("ICT1501", 45, "Reviewing IP subnetting mask calculations.")
    
    stats = tracker.get_focus_stats()
    
    print("\n----------------------------------------")
    print("STUDENT FOCUS & GAMIFICATION PROFILE:")
    print(f"Total Focus Time: {stats['total_time']}")
    print(f"Total Study Sprints: {stats['total_sessions']}")
    print(f"Total Study XP: {stats['total_xp']} XP")  # Fixed key here!
    print(f"Active Streak: {stats['streak']} sessions")
    print("----------------------------------------")