from crewai import Agent


def create_itinerary_agent(llm):

    return Agent(
        role="Itinerary Planning Agent",
        goal="Create a practical day-by-day travel itinerary.",
        backstory=(
            "You are an expert itinerary planner. "
            "You organize activities efficiently across each day "
            "while considering travel time, interests, food and budget."
        ),
        llm=llm,
        verbose=False
    )