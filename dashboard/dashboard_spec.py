from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List, Optional, Literal, Dict
import json
import os

# Define Metadata Path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METADATA_PATH = os.path.join(BASE_DIR, "../data/processed/metadata.json")

def load_metadata():
    if not os.path.exists(METADATA_PATH):
        # Fallback or error if metadata not found (e.g. during initial testing)
        return {"allowed_yearmonths": [], "allowed_countries": [], "capabilities": {"slots": []}}
    with open(METADATA_PATH, "r") as f:
        return json.load(f)

# Load metadata once at module level or usage time? 
# Better to load dynamically or lazily to ensure fresh data.

class DashboardFilters(BaseModel):
    YearMonth: List[str] = Field(default_factory=list, description="List of YearMonths to filter by (e.g. ['2011-01'])")
    Country: List[str] = Field(default_factory=list, description="List of Countries to filter by (e.g. ['France'])")

class VisualConfig(BaseModel):
    visible: bool = True
    mode: Optional[str] = None
    metric: Optional[str] = None

class DashboardVisuals(BaseModel):
    slot_kpi_cards: Optional[VisualConfig] = Field(default_factory=VisualConfig)
    slot_trend: Optional[VisualConfig] = Field(default_factory=VisualConfig)
    slot_top_countries: Optional[VisualConfig] = Field(default_factory=VisualConfig)
    slot_top_products: Optional[VisualConfig] = Field(default_factory=VisualConfig)

class DashboardSpec(BaseModel):
    dashboard_title: str
    filters: DashboardFilters
    visuals_config: DashboardVisuals

    @model_validator(mode='after')
    def validate_values(self):
        metadata = load_metadata()
        allowed_ym = set(metadata.get("allowed_yearmonths", []))
        allowed_countries = set(metadata.get("allowed_countries", []))
        allowed_slots = set(metadata.get("capabilities", {}).get("slots", []))

        # Validate YearMonth
        for ym in self.filters.YearMonth:
            if ym not in allowed_ym:
                raise ValueError(f"Invalid YearMonth: {ym}. Allowed values are in metadata.")

        # Validate Country
        for c in self.filters.Country:
            if c not in allowed_countries:
                raise ValueError(f"Invalid Country: {c}. Allowed values are in metadata.")

        # Validate Visual Slots (Keys in visuals_config are fixed by Pydantic model, 
        # but we could check against metadata if the model was dynamic. 
        # Since model is static, Pydantic handles structure. 
        # We could check if we are *using* slots not supported, but here the model defines support.)
        
        return self

if __name__ == "__main__":
    # Test valid
    try:
        spec = DashboardSpec(
            dashboard_title="Test Dashboard",
            filters={"YearMonth": ["2011-01"], "Country": []},
            visuals_config={"slot_trend": {"visible": True}}
        )
        print("Valid Spec validated successfully.")
    except Exception as e:
        print(f"Validation failed as expected? {e}")

