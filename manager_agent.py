from crewai import Agent


def create_manager(llm):

    return Agent(
        role="Travel Manager",
        goal="Coordinate all travel planning information and create a complete personalized travel plan.",
        backstory=(
            "You are an expert travel planning manager. "
            "You combine research, itinerary, budget, weather, food, hotel "
            "and transportation information into one practical travel plan."
        ),
        llm=llm,
        verbose=False
    )