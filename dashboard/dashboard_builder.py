import os
import shutil
import json
import uuid
from datetime import datetime

# Define paths relative to this script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "template")
OUTPUT_BASE_DIR = os.path.join(BASE_DIR, "output")
MAP_PATH = os.path.join(BASE_DIR, "../docs/template_map.json")

class DashboardBuilder:
    def __init__(self, spec_dict):
        self.spec = spec_dict
        # Create a unique run ID for the output folder
        self.run_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())[:8]
        self.output_dir = os.path.join(OUTPUT_BASE_DIR, self.run_id)
        self.template_map = self._load_map()

    def _load_map(self):
        print(f"Loading template map from: {MAP_PATH}")
        if not os.path.exists(MAP_PATH):
            raise FileNotFoundError(f"Template map not found at {MAP_PATH}")
        with open(MAP_PATH, "r") as f:
            return json.load(f)

    def _copy_template(self):
        print(f"Copying template from {TEMPLATE_DIR} to {self.output_dir}")
        if not os.path.exists(TEMPLATE_DIR):
            raise FileNotFoundError(f"Template directory not found at {TEMPLATE_DIR}")
        
        # Ensure output base directory exists
        os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)
        # Copy the entire template directory tree
        shutil.copytree(TEMPLATE_DIR, self.output_dir)
        print("Template copied successfully.")

    def generate(self):
        """
        Main execution flow.
        For Commit 24: Handles Validation (loading), Copying, and finding target files.
        """
        print(f"Starting dashboard generation for run: {self.run_id}")
        
        # 1. Copy the template folder
        self._copy_template()
        
        # 2. Parse report file path from the template map
        report_path_rel = self.template_map.get("report_file_path")
        if not report_path_rel:
            raise ValueError("report_file_path missing in template_map.json")
        
        target_report_file = os.path.join(self.output_dir, report_path_rel)
        if not os.path.exists(target_report_file):
            raise FileNotFoundError(f"Expected report file not found at {target_report_file}")
             
        # 3. Load the target JSON file to ensure it's readable and ready for edits
        with open(target_report_file, "r") as f:
            report_data = json.load(f)
            print(f"Successfully loaded target report file: {report_path_rel}")
             
        # Modifications to report_data will be implemented in Commit 25
        
        return self.output_dir

if __name__ == "__main__":
    # Test execution for Commit 24
    try:
        dummy_spec = {
            "dashboard_title": "Test run",
            "filters": {"YearMonth": [], "Country": []},
            "visuals_config": {}
        }
        print("Initializing Builder with Dummy Spec...")
        builder = DashboardBuilder(dummy_spec)
        output_path = builder.generate()
        print(f"\nSuccess! Output saved to: {output_path}")
    except Exception as e:
        print(f"Error during execution: {e}")
