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
                        "startDate": data.get("courseStartDate"),
                        "fee": data.get("fee"),
                        "discount": data.get("discount"),
                        "medium": data.get("medium"),
                        "introVideo": data.get("introVideo"),
                        "examDates": {
                            "main": data.get("examDate"),
                            "RA1": data.get("examDateRAI"),
                            "RA2": data.get("examDateRA2")
                        },
                        "coverImageUrl": data.get("coverImage", {}).get("url", ""),
                        "syllabus": data.get("syllabus", {}).get("url", ""),
                        "resources": data.get("courseResources", []),
                        "requirements": data.get("requirements", {}).get("en", ""),
                        "outcomes": data.get("outcomes", {}).get("en", ""),
                        "description": data.get("description", {}).get("en", "")
                    }
                }

        return {"status": "error", "message": "Course not found."}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
