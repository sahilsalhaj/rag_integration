from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_student_details(usn):
    """Fetch student details by USN."""
    response = supabase.table("interview_stats").select("*").eq("usn", usn).execute()

    if response.data:  # Ensure it is not None or empty
        return response.data[0] if len(response.data) > 0 else None
    return None

