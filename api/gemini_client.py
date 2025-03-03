import google.generativeai as genai
from api.config import GEMINI_API_KEY

# Configure Gemini AI
genai.configure(api_key=GEMINI_API_KEY)

def generate_summary(student_data, rounds_analysis=None):  # Added `rounds_analysis`
    """Generate a structured AI-based student interview summary."""

    if not student_data:
        return "No interview records found."

    # Case 1: If a company is specified, process single-record summary
    if isinstance(student_data, dict) and 'company_name' in student_data:
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
            "HR Round": student_data.get("hr_round"),
        }

        rounds_cleared = [k for k, v in rounds.items() if v]
        rounds_failed = [k for k, v in rounds.items() if v is False]

        prompt = f"""
        Generate a structured summary for the student based on their interview progress:

        - USN: {student_data['usn']}
        - Name: {student_data['student_info']['name']}
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

    # Case 2: If no company is specified, generate a consolidated summary
    elif isinstance(student_data, list):  
        total_attempts = len(student_data)
        total_placed = sum(1 for record in student_data if record.get("placed"))
        placement_rate = (total_placed / total_attempts) * 100 if total_attempts > 0 else 0

        # Use provided rounds_analysis if available
        rounds_summary = rounds_analysis or "No round data available."

        prompt = f"""
        Provide a structured and consistent performance summary for {student_data[0]['usn']} across all companies.

        ## Student Overview:
        - **Name:** {student_data[0]['student_info']['name']}
        - **Total Companies Applied:** {total_attempts}
        - **Total Companies Placed:** {total_placed}
        - **Placement Rate:** {placement_rate:.2f}%

        ## Interview Rounds Analysis:
        {rounds_summary}

        ## Performance Insights:
        - **Strengths:** Identify key areas where the student excels.
        - **Weaknesses:** Highlight struggles in certain rounds.
        - **Areas for Improvement:** Suggest ways to improve performance.

        **Ensure the response follows this exact structure every time, including all section headers and formatting.**
        """


    else:
        return "Invalid data format."

    model = genai.GenerativeModel("gemini-2.0-flash-lite")
    
    response = model.generate_content(prompt)

    return response.text if response and hasattr(response, "text") else "No summary available."
