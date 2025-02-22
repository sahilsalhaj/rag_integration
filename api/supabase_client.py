from supabase import create_client
from api.config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_all_companies():
    """Fetch all distinct company names from the database."""
    response = supabase.table("interview_stats").select("company_name").execute()
    if response.data:
        return {row["company_name"].lower() for row in response.data}
    return set()

def get_student_details(usn, company=None):
    try:
        query = supabase.table("interview_stats").select("*").eq("usn", usn)

        if company:
#            query = query.eq("company_name", company)  # Filter for specific company
            query = query.ilike("company_name", company.lower())  # Ensure both are lowercase

        response = query.execute()
        data = response.data

        return data if data else None  # Return data or None if no record found

    except Exception as e:
        return None



