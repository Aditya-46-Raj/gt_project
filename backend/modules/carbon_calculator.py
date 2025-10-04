import json
import os

def load_material_db():
    """Loads the material database from its JSON file."""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(dir_path, '../../data/material_db.json')
    with open(db_path, "r") as f:
        return json.load(f)

def calculate_carbon(blueprint_data):
    """Calculates the carbon footprint based on parsed blueprint data."""
    db = load_material_db()
    total = 0
    materials_report = []
    fallback_emission_factor = 0.5 

    for room in blueprint_data.get("rooms", []):
        # --- THIS IS THE CORRECTED SECTION ---
        # We now get the 'name' from the room data, along with material and area.
        name = room.get("name", "Unknown Area")
        mat = room.get("material", "unknown")
        area = room.get("area", 0)

        emission_factor = db.get(mat, fallback_emission_factor)
        
        emission = area * emission_factor
        total += emission
        
        # We now add the 'name' key to the dictionary we create.
        materials_report.append({
            "name": name, # The added key
            "material": mat,
            "quantity": area,
            "unit": "sqft",
            "emission": emission
        })
        # --- END OF CORRECTION ---

    return {
        "materials": materials_report,
        "total_emissions": total
    }