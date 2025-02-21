from flask import Flask, request, jsonify, render_template
from supabase_client import get_student_details
from gemini_client import generate_summary

app = Flask(__name__)

def extract_usn(query):
    words = query.split()
    for word in words:
        if word.upper().startswith("1NH"):
            return word.upper()
    return None

@app.route("/")
def home():
    return "Hello welcome to rag project"

@app.route("/query", methods=["POST"])
def process_query():
    data = request.get_json()
    
    if not data or "query" not in data:
        return jsonify({"error": "Invalid request. 'query' is required."}), 400

    user_query = data["query"]
    usn = extract_usn(user_query)

    if not usn:
        return jsonify({"error": "Could not identify a valid USN in the query."}), 400

    student_data = get_student_details(usn)
    if not student_data:
        return jsonify({"error": "Student not found."}), 404

    summary = generate_summary(student_data)
    return jsonify({"response": summary})
