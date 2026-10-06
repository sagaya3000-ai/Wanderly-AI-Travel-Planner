from crewai import Agent


def create_budget_agent(llm):

    return Agent(
        role="Budget Agent",
        goal="Create a realistic travel budget that stays close to the user's limit.",
        backstory=(
            "You are a travel budget specialist. "
            "You estimate transportation, accommodation, food and activity "
            "costs and help travelers stay within their budget."
        ),
        llm=llm,
        verbose=False
    )