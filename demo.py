import os
import sys
import json

# Add project root to path for imports
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from llm_engine.gemini_client import GeminiClient
from llm_engine.prompts import build_dashboard_prompt
from dashboard.dashboard_spec import DashboardSpec, load_metadata
from dashboard.dashboard_builder import DashboardBuilder

def main():
    print("--- AI-powered Analytics Dashboard Generator ---")
    
    # 1. Get User Input
    user_query = input("Enter your dashboard request (e.g., 'Show me France in March 2011'): ")
    if not user_query.strip():
        print("Empty request. Exiting.")
        return

    # 2. Load Metadata (Allowed Values)
    try:
        metadata = load_metadata()
        print(f"Loaded {len(metadata.get('allowed_yearmonths', []))} allowed months and {len(metadata.get('allowed_countries', []))} countries.")
    except Exception as e:
        print(f"Error loading metadata: {e}. Please ensure Step 20 (allowed_values.py) was run.")
        return

    # 3. Prepare schema context
    # Pydantic v2 schema generation
    schema_str = json.dumps(DashboardSpec.model_json_schema(), indent=2)

    # 4. Generate Prompt
    prompt = build_dashboard_prompt(user_query, metadata, schema_str)

    # 5. Call Gemini
    try:
        client = GeminiClient()
        print("\nSending request to Gemini Architect...")
        raw_spec_dict = client.generate_dashboard_spec(user_query, schema_str)
        print("\nGemini generated specification:")
        print(json.dumps(raw_spec_dict, indent=2))
    except Exception as e:
        print(f"\nFailed to generate spec from Gemini: {e}")
        print("Check your GOOGLE_API_KEY in .env and network connection.")
        return

    # 6. Validate Spec
    try:
        print("\nValidating Spec against Schema and Allowed Values...")
        validated_spec = DashboardSpec(**raw_spec_dict)
        print("Validation Successful!")
    except Exception as e:
        print(f"\nValidation Failed. The AI generated an invalid configuration:\n{e}")
        return

    # 7. Run Builder
    try:
        print("\nStarting Dashboard Builder...")
        # Pass the validated dictionary back to the builder
        builder = DashboardBuilder(validated_spec.model_dump())
        output_path = builder.generate()
        
        print("\n" + "="*50)
        print("SUCCESS! Dashboard Generated.")
        print("="*50)
        print(f"Location: {output_path}")
        print(f"Open '{output_path}/RetailAnalysis.pbip' in Power BI Desktop.")
        
    except Exception as e:
         print(f"\nBuilder Error: {e}")

if __name__ == "__main__":
    main()
