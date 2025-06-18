# kalix/main.py
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")
from agent.kalix_agent import run_kalix_agent
from calendar_integration.calendar_handler import get_upcoming_events


def main():
    print("🤖 Kalix is running. Type your message:")
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break
        response = run_kalix_agent(user_input)
        # response is a dict, print only the "output" field
        print(f"Kalix: {response.get('output', response)}")

        if user_input.lower() == "show my calendar_integration":
            print("📅 Upcoming events:")
            print(get_upcoming_events())
        else:
            output = run_kalix_agent(user_input)

if __name__ == "__main__":
    main()
