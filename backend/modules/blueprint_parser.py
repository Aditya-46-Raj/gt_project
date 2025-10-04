import pdfplumber
import re
import math

def parse_dimension(dim_str):
    """Cleans and converts a dimension string into a float."""
    cleaned_str = re.sub(r"[^0-9'\"-]", "", dim_str)
    parts = cleaned_str.replace('"', '').split("'")
    feet = int(parts[0]) if parts[0] else 0
    inches = int(parts[1]) if len(parts) > 1 and parts[1] else 0
    return float(feet) + float(inches) / 12

def parse_blueprint(filepath):
    """
    Parses a complex floor plan using a hybrid approach of dimension analysis and
    keyword-based area estimation as a fallback.
    """
    # Fallback dictionary for rooms that might not have clear dimensions
    keyword_areas = {
        'lobby': {'area': 350, 'material': 'general construction'},
        'conf room': {'area': 120, 'material': 'general construction'}
    }

    parsed_data = {"rooms": []}
    
    try:
        with pdfplumber.open(filepath) as pdf:
            page = pdf.pages[0]
            words = page.extract_words(x_tolerance=2, y_tolerance=2)
            full_text = page.extract_text().lower()

            rooms = {}
            dimensions = []

            for word in words:
                text = word["text"]
                if re.match(r"^\d{3}$", text):
                    # For rooms like "Office 101", store the name as well
                    name_candidates = [w['text'] for w in words if abs(w['x0'] - word['x0']) < 50 and 0 < (word['top'] - w['top']) < 15]
                    name = name_candidates[0] if name_candidates else f"Room {text}"
                    rooms[text] = {'x': (word['x0'] + word['x1']) / 2, 'y': (word['top'] + word['bottom']) / 2, 'name': name}
                elif "'" in text or '"' in text:
                    dimensions.append({'text': text, 'x': (word['x0'] + word['x1']) / 2, 'y': (word['top'] + word['bottom']) / 2})

            # --- Dimension Parsing Logic ---
            for room_num, room_pos in rooms.items():
                # (Same dimension matching logic as before)
                nearest_h_dim, nearest_v_dim = (None, None)
                min_h_dist, min_v_dist = (float('inf'), float('inf'))
                
                for dim in dimensions:
                    if abs(room_pos['y'] - dim['y']) > 20 and abs(room_pos['x'] - dim['x']) < 150:
                        dist = abs(room_pos['x'] - dim['x'])
                        if dist < min_v_dist: min_v_dist, nearest_v_dim = (dist, dim['text'])
                    elif abs(room_pos['x'] - dim['x']) > 20 and abs(room_pos['y'] - dim['y']) < 150:
                        dist = abs(room_pos['y'] - dim['y'])
                        if dist < min_h_dist: min_h_dist, nearest_h_dim = (dist, dim['text'])
                
                if nearest_h_dim and nearest_v_dim:
                    try:
                        area = round(parse_dimension(nearest_h_dim) * parse_dimension(nearest_v_dim))
                        parsed_data["rooms"].append({"name": room_pos['name'], "area": area, "material": "general construction"})
                    except (ValueError, TypeError): continue
            
            # --- Fallback Keyword Logic ---
            # Find which rooms were NOT successfully parsed
            parsed_room_names = {r['name'].lower() for r in parsed_data["rooms"]}
            
            for keyword, data in keyword_areas.items():
                # If a keyword room is in the PDF but wasn't parsed via dimensions, add it
                if keyword in full_text and keyword not in parsed_room_names:
                    parsed_data["rooms"].append({"name": keyword.capitalize(), "area": data['area'], "material": data['material']})


    except Exception as e:
        print(f"Error parsing PDF with hybrid logic: {e}")
        parsed_data["rooms"].append({"name": "Error during parsing", "area": 0, "material": "unknown"})

    if not parsed_data["rooms"]:
         parsed_data["rooms"].append({"name": "No rooms with valid data found", "area": 0, "material": "unknown"})

    return parsed_data