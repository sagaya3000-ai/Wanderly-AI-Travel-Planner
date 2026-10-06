from crewai import Agent


def create_food_agent(llm):

    return Agent(
        role="Food and Restaurant Agent",
        goal="Recommend local food, famous dishes and suitable food areas.",
        backstory=(
            "You are a food travel specialist. "
            "You know about local dishes, popular food areas and "
            "food experiences suitable for different travelers."
        ),
        llm=llm,
        verbose=False
    )