from crewai import Agent


def create_weather_agent(llm):

    return Agent(
        role="Weather Agent",
        goal="Provide useful weather-related travel guidance.",
        backstory=(
            "You are a travel weather advisor. "
            "You provide general weather guidance and preparation tips "
            "for travelers based on their destination and travel dates."
        ),
        llm=llm,
        verbose=False
    )