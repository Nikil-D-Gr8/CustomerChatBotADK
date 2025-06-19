import firebase_admin
from firebase_admin import credentials, firestore



def query_courses(
    filter_by: dict = {},
    fields: list = [],
) -> dict:
    """
    Query courses from the database based on optional filters and return selected fields.

    Args:
        filter_by (dict): Optional dictionary to filter courses, e.g. {"courseId": "cict_english_a1"}.
        fields (list): Optional list of fields to return. E.g. ["courseName", "courseDuration"].
                       If empty, all fields will be returned.

    Returns:
        dict: A dictionary with the status and a list of matched courses with requested fields.
    """

    if not firebase_admin._apps:
        cred = credentials.Certificate("firestore.json")
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    courses_ref = db.collection("courses")

    try:
        results = []

        for doc in courses_ref.stream():
            data = doc.to_dict()

            # Filter based on provided key-value pairs
            match = True
            for key, value in filter_by.items():
                if data.get(key) != value:
                    match = False
                    break

            if not match:
                continue

            # Select only requested fields
            if fields:
                filtered_data = {}
                for field in fields:
                    if field == "courseName":
                        filtered_data["courseName"] = data.get("courseName", {}).get("en", "")
                    elif field == "courseOverview":
                        filtered_data["courseOverview"] = data.get("courseOverview", {}).get("en", "")
                    else:
                        filtered_data[field] = data.get(field)
                results.append(filtered_data)
            else:
                # Return entire course data
                course_data = data.copy()
                course_data["courseName"] = data.get("courseName", {}).get("en", "")
                course_data["courseOverview"] = data.get("courseOverview", {}).get("en", "")
                results.append(course_data)

        if not results:
            return {"status": "error", "error_message": "No matching courses found."}

        return {"status": "success", "courses": results}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}
