from google.adk.agents import Agent
from multi_tool_agent.firebase_client import get_firestore_client
import difflib


# ✅ Tool 1: Just fetch all available courses
def find_available_courses() -> dict:
    db = get_firestore_client()
    courses_ref = db.collection("courses")

    courses = []
    try:
        for doc in courses_ref.stream():
            data = doc.to_dict()
            name = data.get("courseName", {}).get("en", "")
            course_id = data.get("courseId", "")
            if name and course_id:
                courses.append({
                    "courseId": course_id,
                    "courseName": name
                })

        if not courses:
            return {"status": "error", "error_message": "No courses found."}

        return {"status": "success", "courses": courses}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


# ✅ Tool 2: Describe a course by ID
def describe_course(course_id: str) -> dict:
    db = get_firestore_client()
    courses_ref = db.collection("courses")
    try:
        for doc in courses_ref.stream():
            data = doc.to_dict()
            if data.get("courseId") == course_id:
                return {
                    "status": "success",
                    "course": {
                        "name": data.get("courseName", {}).get("en", ""),
                        "overview": data.get("courseOverview", {}).get("en", ""),
                        "duration": data.get("courseDuration"),
                        "classesPerWeek": data.get("classesPerWeek"),
                        "batch": data.get("batch")
                    }
                }

        return {"status": "error", "error_message": "Course not found."}

    except Exception as e:
        return {"status": "error", "error_message": str(e)}


# ✅ Agent Definition
root_agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.0-flash",
    description="Agent that helps users find and learn more about available courses.",
    instruction=(
        "Start by calling the tool to get the list of all courses. "
        "Then ask the user what kind of course they’re interested in (e.g. language, topic, level). "
        "Match their interest to a course name from the list and recommend the best fit. "
        "If the user asks for details, call the describe_course tool with the matching course ID. "
        "If they’re not satisfied with the first recommendation, suggest another one from the list."
    ),
    tools=[find_available_courses, describe_course],
)
