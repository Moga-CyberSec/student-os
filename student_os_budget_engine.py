import datetime
import json
import os

class StudentBudgetEngine:
    def __init__(self, student_name, total_allowance, payout_date, next_payout_date, storage_file="student_budget.json"):
        self.student_name = student_name
        self.total_allowance = float(total_allowance)
        self.payout_date = datetime.datetime.strptime(payout_date, "%Y-%m-%d").date()
        self.next_payout_date = datetime.datetime.strptime(next_payout_date, "%Y-%m-%d").date()
        self.storage_file = storage_file
        self.expenses = []
        self.fixed_costs = 0.0
        
        # Load existing data if file exists
        self.load_data()

    def add_fixed_cost(self, name, amount):
        self.fixed_costs += float(amount)
        print(f"[+] Added Fixed Cost: {name} (R{amount:.2f})")

    def calculate_days_remaining(self, current_date_str=None):
        today = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date() if current_date_str else datetime.date.today()
        days_left = (self.next_payout_date - today).days
        return max(days_left, 1)

    def log_expense(self, category, amount, description=""):
        expense_entry = {
            "category": category,
            "amount": float(amount),
            "description": description,
            "date": str(datetime.date.today())
        }
        self.expenses.append(expense_entry)
        self.save_data()
        print(f"[-] Expense Logged & Saved: {category} - R{amount:.2f} ({description})")

    def get_total_spent(self):
        return sum(exp["amount"] for exp in self.expenses) + self.fixed_costs

    def calculate_safe_to_spend_daily(self, current_date_str=None):
        days_remaining = self.calculate_days_remaining(current_date_str)
        total_spent = self.get_total_spent()
        remaining_balance = self.total_allowance - total_spent

        if remaining_balance <= 0:
            return 0.0, days_remaining, "CRITICAL: Allowance depleted! Activate peer meal-share credits."

        daily_limit = remaining_balance / days_remaining
        warning_msg = "ON TRACK" if daily_limit >= 30.0 else "WARNING: Low daily allowance. Consider joining the Res Grocery Pool!"
        
        return daily_limit, days_remaining, warning_msg

    def save_data(self):
        """Saves current budget state to a local JSON file."""
        data = {
            "student_name": self.student_name,
            "total_allowance": self.total_allowance,
            "fixed_costs": self.fixed_costs,
            "expenses": self.expenses
        }
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        """Loads previous expenses from local file if it exists."""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    data = json.load(f)
                    self.expenses = data.get("expenses", [])
                    print(f"[i] Loaded {len(self.expenses)} past expenses from local file ({self.storage_file}).")
            except Exception as e:
                print(f"[!] Could not load storage file: {e}")

# ==========================================
# EXECUTION TEST
# ==========================================
if __name__ == "__main__":
    print("=== STUDENT OS: PERSISTENT BUDGET ENGINE ===")
    
    student = StudentBudgetEngine(
        student_name="Umongezi Mathabela",
        total_allowance=1650.00,
        payout_date="2026-10-01",
        next_payout_date="2026-10-31"
    )
    
    # Check if we want to log a new test expense
    student.log_expense("Transport", 25.00, "Taxi fare to campus library")
    
    simulated_today = "2026-10-15"
    daily_limit, days_left, status = student.calculate_safe_to_spend_daily(simulated_today)
    
    print("\n----------------------------------------")
    print(f"Student: {student.student_name}")
    print(f"Days Until Next Allowance: {days_left} days")
    print(f"Total Spent So Far (Including Saved): R{student.get_total_spent():.2f}")
    print(f"SAFE-TO-SPEND DAILY LIMIT: R{daily_limit:.2f} / day")
    print(f"Status: {status}")
    print("----------------------------------------")