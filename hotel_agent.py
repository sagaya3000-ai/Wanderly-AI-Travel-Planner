from crewai import Agent


def create_hotel_agent(llm):

    return Agent(
        role="Hotel Agent",
        goal="Recommend suitable accommodation areas and hotel types.",
        backstory=(
            "You are an accommodation specialist. "
            "You recommend practical hotel areas and accommodation types "
            "based on the destination, number of travelers and budget."
        ),
        llm=llm,
        verbose=False
    )