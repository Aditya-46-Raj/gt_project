# --- DICTIONARIES FOR RECOMMENDATIONS ---

SUGGESTIONS = {
    "concrete": [
        "**Material**: Consider replacing some concrete structures with Mass Timber (like Cross-Laminated Timber, CLT), which sequesters carbon.",
        "**Material**: Specify the use of low-carbon concrete mixes, such as those containing fly ash or slag (SCMs)."
    ],
    "steel": [
        "**Material**: Specify Electric Arc Furnace (EAF) recycled steel instead of virgin steel.",
        "**Material**: Look for opportunities to use engineered wood or advanced composites in place of steel structural elements."
    ]
}

POSITIVE_REINFORCEMENT = {
    "wood": "**Material**: Great choice using wood! Ensure it is sustainably sourced (e.g., FSC or PEFC certified)."
}

# --- NEW: Design suggestions based on room type ---
DESIGN_SUGGESTIONS = {
    "office": [
        "**Design**: Orient office windows to maximize natural daylight, reducing the need for artificial lighting and improving occupant well-being.",
        "**Design**: Consider an open-plan layout with modular furniture to create a flexible space that can be adapted in the future without major renovations."
    ],
    "reception": [
        "**Design**: Incorporate a 'green wall' or large indoor plants in the reception area. This improves air quality and creates a welcoming, biophilic aesthetic.",
    ],
    "general": [ # General design tips if specific rooms aren't identified
        "**Design**: Implement passive design strategies like building orientation and window placement to optimize for natural heating, cooling, and light.",
        "**Design**: Design for deconstruction. Plan how building components can be disassembled and reused at the end of the building's life."
    ]
}

GENERAL_TIPS = [
    "**Construction**: Implement a strict waste management plan to sort and recycle materials on-site.",
    "**Construction**: Prioritize sourcing materials from local suppliers to reduce transport-related emissions."
]

def suggest_reductions(carbon_report):
    """
    Generates a holistic set of recommendations covering materials, design, and construction.
    """
    recommendations = []
    design_recs = []
    materials_used = set()
    rooms_identified = set()

    for item in carbon_report.get("materials", []):
        material = item["material"]
        room_name = item["name"].lower() # Get the room name (e.g., "Office")

        # --- Generate Material-Specific Recommendations ---
        if material not in materials_used:
            if material in SUGGESTIONS:
                recommendations.extend(SUGGESTIONS[material])
            if material in POSITIVE_REINFORCEMENT:
                recommendations.append(POSITIVE_REINFORCEMENT[material])
            materials_used.add(material)

        # --- Generate Design Recommendations based on Room Type ---
        # Find a keyword from the room name (e.g., "office" in "office 101")
        for room_keyword in DESIGN_SUGGESTIONS.keys():
            if room_keyword in room_name and room_keyword not in rooms_identified:
                design_recs.extend(DESIGN_SUGGESTIONS[room_keyword])
                rooms_identified.add(room_keyword)

    # Add general design tips if no specific ones were found
    if not design_recs:
        design_recs.extend(DESIGN_SUGGESTIONS["general"])

    # --- Assemble the Final Report ---
    final_report = []
    if recommendations:
        final_report.append("--- Material Suggestions ---")
        final_report.extend(recommendations)
    
    if design_recs:
        final_report.append("--- Blueprint & Design Enhancements ---")
        final_report.extend(design_recs)

    final_report.append("--- General Construction Practices ---")
    final_report.extend(GENERAL_TIPS)
    
    return final_report