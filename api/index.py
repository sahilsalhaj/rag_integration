from flask import Flask, request, jsonify, render_template
from api.supabase_client import get_student_details,get_all_companies
from api.gemini_client import generate_summary
import re

app = Flask(__name__)
COMPANY_NAMES = get_all_companies()  # Store lowercase names for easy matching

# def extract_company_name(query):
#     keywords = ["in", "at", "for", "from", "of"]
#     words = query.split()

#     for i, word in enumerate(words):
#         if word.lower() in keywords and i < len(words) - 1:
#             return words[i + 1].lower()  # Assume next word is company name

#     return None  # No company specified
def extract_company_name(query):
    words = query.lower().split()
    
    for size in range(3, 0, -1):  # Try matching 3-word, 2-word, then 1-word names
        for i in range(len(words) - size + 1):
            phrase = " ".join(words[i:i + size])  # Extract potential name
            if phrase in COMPANY_NAMES:  # Match against known company names
                return phrase  # Return matched company name
    return None

def extract_usn(query):
    words = query.split()
    for word in words:
        if word.upper().startswith("1NH"):
            return word.upper()
    return None

@app.route("/")
def home():
    return render_template("templates/index.py")

# @app.route("/query", methods=["POST"])
# def process_query():
#     data = request.get_json()
    
#     if not data or "query" not in data:
#         return jsonify({"error": "Invalid request. 'query' is required."}), 400

#     user_query = data["query"]
#     usn = extract_usn(user_query)

#     if not usn:
#         return jsonify({"error": "Could not identify a valid USN in the query."}), 400

#     student_data = get_student_details(usn)
#     if not student_data:
#         return jsonify({"error": "Student not found."}), 404

#     summary = generate_summary(student_data)
#     return jsonify({"response": summary})
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

    # Extract company name
    company = extract_company_name(user_query)

    student_data = get_student_details(usn, company)

    if not student_data:
        return jsonify({"error": "No records found for the student."}), 404

    # If multiple records exist, generate summaries for all companies
    # Handle multiple company records
    if isinstance(student_data, list):
        summaries = {record["company_name"]: generate_summary(record) for record in student_data}
        return jsonify({"response": summaries if len(summaries) > 1 else list(summaries.values())[0]})

    
    # If only one record exists, return that summary
    summary = generate_summary(student_data[0]) if isinstance(student_data, list) else generate_summary(student_data)
    return jsonify({"response": summary})

