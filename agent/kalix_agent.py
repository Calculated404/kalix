# kalix/agent/kalix_agent.py

from langchain.agents import initialize_agent, Tool, AgentType
from langchain_ollama import ChatOllama
from tools.node_red import control_device
from memory.memory import memory
from tools.calendar_tool import calendar_summary
from langchain.tools import Tool
from tools.calendar_tool import create_event

llm = ChatOllama(model="llama3")


tools = [
    Tool(
         name="CreateCalendarEvent",
         func=lambda tool_input: create_event(tool_input),
        description="Use this to create an event on the user's Google Calendar. The input should contain a date, time, and event description."
    ),
    Tool(
        name="CalendarSummary",
        func=lambda tool_input: calendar_summary(tool_input),
        description="Use this to get a summary of upcoming calendar events. Provide a time range or question like 'next week' or 'tomorrow'."
    ),
    Tool(
        name="SmartHomeControl",
        func=control_device,
        description="Use this to control smart home devices by sending commands like 'turn on the kitchen lights'"
    )
]

agent_with_memory = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    agent_kwargs={
        "system_message": "You are Kalix, a smart home AI assistant. Always use tools when asked about calendars, smart home devices, or external actions. Don't make up answers — use the right tool instead."
    }
)

def run_kalix_agent(user_input: str):
    return agent_with_memory.invoke({"input": user_input})
