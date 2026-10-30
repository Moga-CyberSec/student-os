import datetime
import json
import os

class AcademicHubEngine:
    def __init__(self, storage_file="academic_hub.json"):
        self.storage_file = storage_file
        self.modules = []
        self.assignments = []
        self.load_data()

    def add_module(self, module_code, module_name, lecturer=""):
        """Registers a university module."""
        module_entry = {
            "code": module_code.upper(),
            "name": module_name,
            "lecturer": lecturer
        }
        # Avoid duplicate module codes
        if not any(m["code"] == module_entry["code"] for m in self.modules):
            self.modules.append(module_entry)
            self.save_data()
            print(f"[+] Module Registered: {module_code} - {module_name}")
        else:
            print(f"[i] Module {module_code} already registered.")

    def add_assignment(self, module_code, title, due_date_str, description=""):
        """Adds an assignment or project deadline for a module."""
        assignment_entry = {
            "id": len(self.assignments) + 1,
            "module_code": module_code.upper(),
            "title": title,
            "due_date": due_date_str,
            "description": description,
            "completed": False
        }
        self.assignments.append(assignment_entry)
        self.save_data()
        print(f"[+] Assignment Tracked: [{module_code}] {title} (Due: {due_date_str})")

    def complete_assignment(self, assignment_id):
        """Marks an assignment as completed."""
        for assign in self.assignments:
            if assign["id"] == assignment_id:
                assign["completed"] = True
                self.save_data()
                print(f"[✓] Assignment Completed: {assign['title']}")
                return True
        print(f"[!] Assignment ID {assignment_id} not found.")
        return False

    def get_upcoming_deadlines(self, current_date_str=None):
        """Calculates days remaining for all uncompleted assignments."""
        today = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date() if current_date_str else datetime.date.today()
        upcoming = []
        
        for assign in self.assignments:
            if not assign["completed"]:
                due = datetime.datetime.strptime(assign["due_date"], "%Y-%m-%d").date()
                days_left = (due - today).days
                upcoming.append({
                    "id": assign["id"],
                    "title": assign["title"],
                    "module": assign["module_code"],
                    "due_date": assign["due_date"],
                    "days_left": days_left
                })
        
        # Sort by closest deadline first
        upcoming.sort(key=lambda x: x["days_left"])
        return upcoming

    def save_data(self):
        """Saves academic data locally to JSON."""
        data = {
            "modules": self.modules,
            "assignments": self.assignments
        }
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        """Loads saved modules and assignments from local storage."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    data = json.load(f)
                    self.modules = data.get("modules", [])
                    self.assignments = data.get("assignments", [])
            except Exception as e:
                print(f"[!] Error loading academic data: {e}")

# ==========================================
# TEST RUN: ACADEMIC HUB SIMULATION
# ==========================================
if __name__ == "__main__":
    print("=== STUDENT OS: ACADEMIC HUB ENGINE ===")
    
    hub = AcademicHubEngine()
    
    # 1. Register modules
    hub.add_module("ICT1501", "Communications Networks I", "Department of ICT")
    hub.add_module("PRG1501", "Development Software (Java/Python)", "Department of IT")
    
    # 2. Add upcoming assignments (simulating future deadlines)
    hub.add_assignment("ICT1501", "Subnetting & IP Addressing Lab", "2026-11-05", "Submit packet tracer lab report.")
    hub.add_assignment("PRG1501", "Object-Oriented CLI Project", "2026-11-12", "Final Java repository push on GitHub.")
    
    # 3. View upcoming deadlines relative to today (simulating Nov 1, 2026)
    simulated_today = "2026-11-01"
    upcoming = hub.get_upcoming_deadlines(simulated_today)
    
    print("\n----------------------------------------")
    print("ACTIVE ASSIGNMENT DEADLINES:")
    for item in upcoming:
        urgency = f"Due in {item['days_left']} days" if item['days_left'] >= 0 else "OVERDUE!"
        print(f"[{item['module']}] ID #{item['id']} - {item['title']} ({urgency})")
    print("----------------------------------------")