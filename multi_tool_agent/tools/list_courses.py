import firebase_admin
from firebase_admin import credentials, firestore

def list_courses() -> dict:
    """
    Returns a list of all available courses with courseId and courseName (in English).
    
    Returns:
        dict: A dictionary with 'status' and 'courses' or an error message.
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate("firestore.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    courses_ref = db.collection("courses")

    try:
        courses = []
        for doc in courses_ref.stream():
            data = doc.to_dict()
            course_id = data.get("courseId", "")
            course_name = data.get("courseName", {}).get("en", "")
            if course_id and course_name:
                courses.append({
                    "courseId": course_id,
                    "courseName": course_name
                })

        if not courses:
            return {"status": "error", "message": "No courses found."}

        return {"status": "success", "courses": courses}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
