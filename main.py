import datetime
import os

# Clean imports from your separate engine files!
from academic_hub_engine import AcademicHubEngine
from career_pipeline_engine import CareerPipelineEngine
from focus_engine import FocusEngine

# (Optional: Import or keep budget logic here)
import json

class StudentOSMaster:
    def __init__(self):
        self.budget_file = "student_budget.json"
        self.load_budget_data()
        
        # Instantiate the imported engine classes
        self.academic_hub = AcademicHubEngine()
        self.focus_engine = FocusEngine()
        self.career_pipeline = CareerPipelineEngine()

    def load_budget_data(self):
        if os.path.exists(self.budget_file):
            with open(self.budget_file, "r") as f:
                self.budget_data = json.load(f)
        else:
            self.budget_data = {
                "student_name": "Umongezi Mathabela",
                "total_allowance": 1650.00,
                "fixed_costs": 150.00,
                "expenses": []
            }

    def save_budget(self):
        with open(self.budget_file, "w") as f:
            json.dump(self.budget_data, f, indent=4)

    # ==========================================
    # PILLAR 1: FINANCIAL LIFEBOAT & RIDE-POOL
    # ==========================================
    def menu_finances(self):
        while True:
            print("\n=== FINANCIAL LIFEBOAT & RIDE-POOL ===")
            print("1. View Allowance & Safe-to-Spend")
            print("2. Log Expense Manually")
            print("3. Calculate & Split P2P Ride-Pool Fare")
            print("4. Return to Main Menu")
            
            choice = input("Select option (1-4): ").strip()
            
            if choice == '1':
                total_spent = sum(e["amount"] for e in self.budget_data["expenses"]) + self.budget_data["fixed_costs"]
                remaining = self.budget_data["total_allowance"] - total_spent
                today = datetime.date.today()
                next_month = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
                days_left = max((next_month - today).days, 1)
                daily_limit = remaining / days_left
                
                print(f"\n--- Financial Status ---")
                print(f"Total Allowance: R{self.budget_data['total_allowance']:.2f}")
                print(f"Total Spent (incl. fixed): R{total_spent:.2f}")
                print(f"Remaining Balance: R{remaining:.2f}")
                print(f"Safe-to-Spend Daily Limit: R{daily_limit:.2f} / day ({days_left} days left)")
            
            elif choice == '2':
                cat = input("Enter category (Transport / Food / Data): ")
                amt = float(input("Enter amount (R): "))
                desc = input("Enter description: ")
                self.budget_data["expenses"].append({
                    "category": cat, "amount": amt, "description": desc, "date": str(datetime.date.today())
                })
                self.save_budget()
                print(f"[✓] Expense of R{amt:.2f} logged successfully!")
            
            elif choice == '3':
                route = input("Enter route name (e.g., Bellville Res to D6 Campus): ")
                fare = float(input("Enter total Bolt/Uber fare (R): "))
                riders = int(input("Enter total number of students sharing: "))
                if riders > 0:
                    split_cost = fare / riders
                    print(f"\n[✓] Split Fare per person: R{split_cost:.2f} (Saved R{fare - split_cost:.2f}!)")
                    log_choice = input("Automatically log this to your budget? (y/n): ").strip().lower()
                    if log_choice == 'y':
                        self.budget_data["expenses"].append({
                            "category": "Transport", "amount": split_cost, "description": f"Ride-Pool: {route}", "date": str(datetime.date.today())
                        })
                        self.save_budget()
                        print("[✓] Ride-pool share logged to budget!")
            
            elif choice == '4':
                break

    # ==========================================
    # PILLAR 2: ACADEMIC HUB (Delegated)
    # ==========================================
    def menu_academics(self):
        while True:
            print("\n=== ACADEMIC HUB ===")
            print("1. View Modules & Deadlines")
            print("2. Add Assignment Deadline")
            print("3. Return to Main Menu")
            
            choice = input("Select option (1-3): ").strip()
            if choice == '1':
                print("\n-- Registered Modules --")
                if not self.academic_hub.modules:
                    print("No modules registered yet.")
                for m in self.academic_hub.modules:
                    print(f"[{m['code']}] {m['name']} (Lecturer: {m['lecturer']})")
                
                print("\n-- Upcoming Assignments --")
                upcoming = self.academic_hub.get_upcoming_deadlines()
                if not upcoming:
                    print("No pending assignments.")
                for a in upcoming:
                    print(f"[{a['module']}] {a['title']} (Due: {a['due_date']} - {a['days_left']} days left)")
            
            elif choice == '2':
                code = input("Enter Module Code (e.g., PRG1501): ")
                title = input("Enter Assignment Title: ")
                due_date = input("Enter Due Date (YYYY-MM-DD): ")
                desc = input("Description: ")
                self.academic_hub.add_assignment(code, title, due_date, desc)
            
            elif choice == '3':
                break

    # ==========================================
    # PILLAR 3: MENTAL & FOCUS ENGINE (Delegated)
    # ==========================================
    def menu_focus(self):
        while True:
            print("\n=== MENTAL & FOCUS ENGINE ===")
            stats = self.focus_engine.get_focus_stats()
            print(f"Focus Time: {stats['total_time']} | XP: {stats['total_xp']} XP | Streak: {stats['streak']} sessions")
            print("1. Log Completed Study Sprint")
            print("2. Return to Main Menu")
            
            choice = input("Select option (1-2): ").strip()
            if choice == '1':
                module = input("Enter module code (e.g., PRG1501): ")
                mins = int(input("Enter duration in minutes: "))
                notes = input("Enter notes: ")
                self.focus_engine.log_focus_session(module, mins, notes)
            elif choice == '2':
                break

    # ==========================================
    # PILLAR 4: CAREER PIPELINE (Delegated)
    # ==========================================
    def menu_career(self):
        while True:
            print("\n=== CAREER PIPELINE & POW LEDGER ===")
            print("1. View Portfolio Projects")
            print("2. Track New Project / Repository")
            print("3. Return to Main Menu")
            
            choice = input("Select option (1-3): ").strip()
            if choice == '1':
                summary = self.career_pipeline.get_portfolio_summary()
                print("\n-- Verified Portfolio --")
                for p in summary['projects']:
                    print(f"[{p['status'].upper()}] {p['name']} ({p['tech_stack']}) -> {p['github_url']}")
            elif choice == '2':
                name = input("Project Name: ")
                stack = input("Tech Stack (e.g., Java / Python): ")
                url = input("GitHub URL: ")
                desc = input("Description: ")
                status = input("Status (In Progress / Deployed / Completed): ")
                self.career_pipeline.add_project(name, stack, url, desc, status)
            elif choice == '3':
                break

    # ==========================================
    # MAIN CLI CONTROLLER
    # ==========================================
    def run(self):
        while True:
            print("\n========================================")
            print("       STUDENT OS: MASTER DASHBOARD     ")
            print("========================================")
            print("1. Financial Lifeboat & P2P Ride-Pool")
            print("2. Academic Hub (Modules & Deadlines)")
            print("3. Mental & Focus Engine (Sprints & XP)")
            print("4. Career Pipeline (Proof-of-Work Ledger)")
            print("5. Exit Student OS")
            
            choice = input("\nSelect a pillar (1-5): ").strip()
            
            if choice == '1':
                self.menu_finances()
            elif choice == '2':
                self.menu_academics()
            elif choice == '3':
                self.menu_focus()
            elif choice == '4':
                self.menu_career()
            elif choice == '5':
                print("\n[i] Shutting down Student OS. Keep building, Umongezi!")
                break
            else:
                print("[!] Invalid choice. Please select between 1 and 5.")

if __name__ == "__main__":
    os_master = StudentOSMaster()
    os_master.run()