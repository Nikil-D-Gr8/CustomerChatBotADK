from firebase_admin import credentials, firestore
import firebase_admin

def get_course_details(course_id: str) -> dict:
    """
    Retrieves full details of a course by its courseId.
    
    Args:
        course_id (str): The courseId to search for.
    
    Returns:
        dict: A dictionary with course details or an error message.
    """
    if not firebase_admin._apps:
        cred = credentials.Certificate("firestore.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    courses_ref = db.collection("courses")

    try:
        for doc in courses_ref.stream():
            data = doc.to_dict()
            if data.get("courseId") == course_id:
                return {
                    "status": "success",
                    "course": {
                        "courseId": course_id,
                        "name": data.get("courseName", {}).get("en", ""),
                        "overview": data.get("courseOverview", {}).get("en", ""),
                        "duration": data.get("courseDuration"),
                        "classesPerWeek": data.get("classesPerWeek"),
                        "batch": data.get("batch"),
                        "startDate": data.get("courseStartDate")[0:10],
                        "fee": data.get("fee"),
                        "medium": data.get("medium"),
                        "examDates": {
                            "main": data.get("examDate")[0:10],
                            # "RA1": data.get("examDateRAI")[0:11],
                            # "RA2": data.get("examDateRA2")[0:11]
                        },
                        "requirements": data.get("requirements", {}).get("en", ""),
                        "outcomes": data.get("outcomes", {}).get("en", ""),
                        "description": data.get("description", {}).get("en", "")
                    }
                }

        return {"status": "error", "message": "Course not found."}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

def list_courses() -> dict:
    """
    Returns a list of all available courses with courseId and courseName (in English).

    Args:
    None, as it will return all courses.
    
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
