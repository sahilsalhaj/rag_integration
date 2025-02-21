import google.generativeai as genai
from api.config import GEMINI_API_KEY

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

def generate_summary(student_data):
    """Generate a detailed AI-based student interview summary from Supabase data."""
    
    rounds = {
        "Resume Screening": student_data.get("resume_screening"),
        "Aptitude": student_data.get("aptitude"),
        "Technical MCQ": student_data.get("technical_mcq"),
        "Coding Round 1": student_data.get("coding_1"),
        "Group Discussion": student_data.get("gd"),
        "Coding Round 2": student_data.get("coding_2"),
        "Technical Interview 1": student_data.get("technical_interview_1"),
        "Technical Interview 2": student_data.get("technical_interview_2"),
        "Assignment": student_data.get("assignment"),
        "Managerial Round": student_data.get("managerial_round"),
        "HR Round": student_data.get("hr_round")
    }
    
    rounds_cleared = [k for k, v in rounds.items() if v]
    rounds_failed = [k for k, v in rounds.items() if v is False]

    prompt = f"""
    Generate a structured summary for the student based on their interview progress:

    - USN: {student_data['usn']}
    - Company: {student_data.get('company_name', 'N/A')}
    - Applied: {'Yes' if student_data.get('applied') else 'No'}
    - Shortlisted: {'Yes' if student_data.get('shortlisted') else 'No'}
    - Attended: {'Yes' if student_data.get('attended') else 'No'}
    - Mode: {'On-Campus' if student_data.get('on_campus') else 'Virtual'}
    
    Interview Rounds Cleared: {', '.join(rounds_cleared) if rounds_cleared else 'None'}
    Interview Rounds Failed: {', '.join(rounds_failed) if rounds_failed else 'None'}
    
    Final Placement Status: {'Placed' if student_data.get('placed') else 'Not Placed'}
    
    Ensure the response is structured, informative, and provides a clear evaluation of the student's performance.
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    
    return response.text if response and hasattr(response, "text") else "No summary available."

