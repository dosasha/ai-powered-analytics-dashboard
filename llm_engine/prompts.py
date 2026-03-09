import json

def build_dashboard_prompt(user_query: str, metadata: dict, json_schema_str: str) -> str:
    """
    Constructs the prompt for Gemini to translate a natural language query 
    into a structured DashboardSpec JSON.
    
    Args:
        user_query (str): The user's request (e.g. "Show me France in March 2011").
        metadata (dict): The allowed values from metadata.json.
        json_schema_str (str): The stringified JSON Schema of DashboardSpec.
        
    Returns:
        str: The complete prompt text.
    """
    
    allowed_ym = metadata.get("allowed_yearmonths", [])
    allowed_countries = metadata.get("allowed_countries", [])
    
    # We provide explicit lists so the LLM knows exactly what's valid.
    prompt = f"""You are an expert Business Intelligence Architect. 
Your task is to translate a user's natural language request into a strict, programmatic JSON configuration for a Dashboard Builder.

### Allowed Data
You may ONLY use the following exact values for filters. If a requested value is not in these lists, do not include it.
- Valid `YearMonth` values (YYYY-MM Format): {allowed_ym}
- Valid `Country` values: {allowed_countries}

### Rules
1. Your response MUST be a VALID JSON object. Do not include markdown formatting like ```json or newlines outside the JSON structure.
2. The JSON MUST strictly conform to the following JSON Schema:
{json_schema_str}
3. `dashboard_title` should be a concise, professional title based on the user's focus (e.g., "Retail Performance - March 2011 Focus").
4. If the user specifies a month (e.g. "March 2011"), set the `YearMonth` filter array to ["2011-03"].
5. If the user specifies a country, set the `Country` filter array.
6. For visual slots (`slot_kpi_cards`, `slot_trend`, `slot_top_countries`, `slot_top_products`), set `visible` to true if they are generally relevant.

### User Request
"{user_query}"

### Output
Return ONLY the raw JSON object. NO conversational text.
"""
    return prompt
