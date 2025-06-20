from google.adk.agents import Agent
from multi_tool_agent.tools.firestore_query import get_course_details,list_courses


root_agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.0-flash",
    description="Agent that helps users interact with course information flexibly.",
    instruction=(
        "Use the 'list_courses' tool to fetch all available courses. "
        "Use the 'get_course_detail' tool to fetch detailed information about a specific course. "
        "You can use the courseId to get details of a specific course."
        "If you need to know about a course, first list all courses and then get the details of the one you are interested in."
        "when the user talks to you, you should first get all the courses and find which course the user is interested in, then get the details of that course." \
        "If the user asks for a course that is not available, you should inform them that the course is not available."
        "If the user asks for a course that is available, you should provide the details of that course."
        "when the user asks for comparison of two courses, you should first get the details of both courses and then compare them based on the user's requirements." \
    ),
    tools=[list_courses,get_course_details],
)
