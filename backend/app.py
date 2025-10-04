import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# --- CORRECTED: Import order and added modules ---
from modules.blueprint_parser import parse_blueprint
from modules.carbon_calculator import calculate_carbon
from modules.recommender import suggest_reductions

# --- CORRECTED: Point static folder to the 'build' directory ---
app = Flask(__name__, static_folder="../frontend/build", static_url_path="/")
CORS(app)

# Define a folder to store uploaded blueprints
UPLOAD_FOLDER = 'data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/api/analyze", methods=["POST"])
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # --- CORRECTED: Use secure_filename to prevent path traversal attacks ---
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Step 1: Parse blueprint (now passes the filepath)
        blueprint_data = parse_blueprint(filepath)

        # Step 2: Carbon calculation
        carbon_report = calculate_carbon(blueprint_data)

        # Step 3: Recommendations
        suggestions = suggest_reductions(carbon_report)

        report = {
            "blueprint_data": blueprint_data,
            "carbon_analysis": carbon_report,
            "recommendations": suggestions,
        }

        return jsonify(report)

    except Exception as e:
        # --- CORRECTED: Added error handling for the whole process ---
        return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500


# Serve React App
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)