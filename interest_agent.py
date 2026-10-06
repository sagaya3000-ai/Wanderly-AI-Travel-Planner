from crewai import Agent


def create_interest_agent(llm):

    return Agent(
        role="Interest Matching Agent",
        goal="Match the traveler's interests with suitable activities and places.",
        backstory=(
            "You are a personalized travel recommendation expert. "
            "You analyze traveler interests and match them with "
            "suitable activities and attractions."
        ),
        llm=llm,
        verbose=False
    )