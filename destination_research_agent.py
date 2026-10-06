from crewai import Agent


def create_destination_agent(llm):

    return Agent(
        role="Destination Research Agent",
        goal="Research important attractions, tourist places and hotspots at the destination.",
        backstory=(
            "You are an experienced destination researcher. "
            "You identify popular attractions and useful places "
            "for travelers based on their interests."
        ),
        llm=llm,
        verbose=False
    )