from flask import Flask, request, jsonify, render_template
from api.supabase_client import get_student_details, get_all_companies
from api.gemini_client import generate_summary
from flask_cors import CORS
import re

app = Flask(__name__, template_folder="../templates")
CORS(app)

COMPANY_NAMES = get_all_companies()  # Store lowercase names for easy matching

def extract_company_name(query):
    words = query.lower().split()
    
    for size in range(3, 0, -1):  # Try matching 3-word, 2-word, then 1-word names
        for i in range(len(words) - size + 1):
            phrase = " ".join(words[i:i + size])  # Extract potential name
            if phrase in COMPANY_NAMES:  # Match against known company names
                return phrase
    return None

def extract_usn(query):
    words = query.split()
    for word in words:
        if word.upper().startswith("1NH"):
            return word.upper()
    return None

@app.route("/")
def home():
#    return "Welcome to the Interview Tracker API!"
    return render_template("index.html")  # Serves the frontend

@app.route("/query", methods=["POST"])
def process_query():
    data = request.get_json()
    
    if not data or "query" not in data:
        return jsonify({"error": "Invalid request. 'query' is required."}), 400

    user_query = data["query"]
    
    # Extract USN
    usn = extract_usn(user_query)
    if not usn:
        return jsonify({"error": "Could not identify a valid USN in the query."}), 400

    # Extract company name (to check if it was mentioned)
    company = extract_company_name(user_query)

    # Fetch student data (either for a specific company or all records)
    student_data = get_student_details(usn, company)

    if not student_data:
        return jsonify({"error": "No records found for the student."}), 404

    # **If a company was explicitly mentioned** → Get summary for that specific company
    if company:
        if isinstance(student_data, list) and len(student_data) == 1:
            student_data = student_data[0]  # Convert single-item list to dict
        summary = generate_summary(student_data)  # Generate single company summary

    # **If no company was mentioned** → Generate a **consolidated** summary
    else:
        if isinstance(student_data, dict):  # If only one record exists, wrap it in a list
            student_data = [student_data]
        summary = generate_summary(student_data)  # Generate consolidated summary

    return jsonify({"response": summary})


if __name__ == "__main__":
    app.run(debug=True)
