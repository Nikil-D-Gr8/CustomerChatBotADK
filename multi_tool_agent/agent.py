from google.adk.agents import Agent
from multi_tool_agent.tools.list_courses import list_courses
from multi_tool_agent.tools.get_course_detail import get_course_detail


root_agent = Agent(
    name="multi_tool_agent",
    model="gemini-2.0-flash",
    description="Agent that helps users interact with course information flexibly.",
    instruction=(
        "Use the 'query_courses' tool to fetch course info. "
        "You can filter using courseId, batch, or any other field, and request only the fields you need. "
        "E.g., just the courseName, or name + duration. Adapt based on user's query."
    ),
    tools=[list_courses,get_course_detail],
)
