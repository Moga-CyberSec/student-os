import datetime
import json
import os

class CareerPipelineEngine:
    def __init__(self, storage_file="career_pipeline.json"):
        self.storage_file = storage_file
        self.projects = []
        self.load_data()

    def add_project(self, project_name, tech_stack, github_url, description, status="In Progress"):
        """Registers a coding project or proof-of-work artifact."""
        project_entry = {
            "id": len(self.projects) + 1,
            "name": project_name,
            "tech_stack": tech_stack,
            "github_url": github_url,
            "description": description,
            "status": status, # In Progress, Deployed, Completed
            "date_added": str(datetime.date.today())
        }
        
        self.projects.append(project_entry)
        self.save_data()
        print(f"[+] Project Tracked: {project_name} [{tech_stack}] - Status: {status}")

    def update_status(self, project_id, new_status):
        """Updates the completion or deployment status of a project."""
        for proj in self.projects:
            if proj["id"] == project_id:
                proj["status"] = new_status
                self.save_data()
                print(f"[✓] Project #{project_id} status updated to: {new_status}")
                return True
        print(f"[!] Project ID {project_id} not found.")
        return False

    def get_portfolio_summary(self):
        total = len(self.projects)
        deployed = sum(1 for p in self.projects if p["status"].lower() == "deployed")
        return {
            "total_projects": total,
            "deployed_projects": deployed,
            "projects": self.projects
        }

    def save_data(self):
        data = {"projects": self.projects}
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, "r") as f:
                    data = json.load(f)
                    self.projects = data.get("projects", [])
            except Exception as e:
                print(f"[!] Error loading career pipeline data: {e}")

# ==========================================
# TEST RUN: CAREER PIPELINE SIMULATION
# ==========================================
if __name__ == "__main__":
    print("=== STUDENT OS: CAREER PIPELINE & POW LEDGER ===")
    
    pipeline = CareerPipelineEngine()
    
    # Track your actual projects
    pipeline.add_project(
        project_name="Password Analyser CLI",
        tech_stack="Java",
        github_url="https://github.com/Moga-CyberSec/password-analyser",
        description="Command-line interface application analyzing password strength and entropy.",
        status="Deployed"
    )
    
    pipeline.add_project(
        project_name="Student OS Ecosystem",
        tech_stack="Python / JSON",
        github_url="https://github.com/Moga-CyberSec/student-os",
        description="Modular local-storage operating system for student finance, transport, and focus.",
        status="In Progress"
    )
    
    summary = pipeline.get_portfolio_summary()
    
    print("\n----------------------------------------")
    print("PROOF-OF-WORK PORTFOLIO SUMMARY:")
    print(f"Total Tracked Projects: {summary['total_projects']}")
    print(f"Deployed to GitHub: {summary['deployed_projects']}")
    print("\nPROJECT LIST:")
    for p in summary['projects']:
        print(f"[{p['status'].upper()}] {p['name']} ({p['tech_stack']}) -> {p['github_url']}")
    print("----------------------------------------")