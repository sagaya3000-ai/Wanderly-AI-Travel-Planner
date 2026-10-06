from crewai import Agent


def create_transportation_agent(llm):

    return Agent(
        role="Transportation Agent",
        goal="Recommend practical transportation options for the journey.",
        backstory=(
            "You are a transportation planning expert. "
            "You recommend suitable ways to travel from the current location "
            "to the destination and useful local transportation options."
        ),
        llm=llm,
        verbose=False
    )