
import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Crew, Process, Task, LLM

from agents.manager_agent import create_manager
from agents.destination_research_agent import create_destination_agent
from agents.itinerary_agent import create_itinerary_agent
from agents.budget_agent import create_budget_agent
from agents.weather_agent import create_weather_agent
from agents.food_agent import create_food_agent
from agents.transportation_agent import create_transportation_agent
from agents.hotel_agent import create_hotel_agent
from agents.interest_agent import create_interest_agent


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("GEMINI_API_KEY is missing in .env file.")
    st.stop()


# =========================================================
# GEMINI LLM
# =========================================================

llm = LLM(
    model="gemini/gemini-3.5-flash-lite",
    api_key=GEMINI_API_KEY,
    temperature=0.3
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Wanderly",
    page_icon="✈️",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #07111f;
        color: white;
    }

    .wanderly-title {
        font-family: Poppins, sans-serif;
        font-size: 42px;
        font-weight: 700;
        color: white;
        margin-bottom: 0px;
    }

    .wanderly-subtitle {
        font-family: Inter, sans-serif;
        font-size: 15px;
        color: #9fb4cc;
        margin-bottom: 20px;
    }

    .route {
        height: 2px;
        background: repeating-linear-gradient(
            to right,
            #2188ff 0px,
            #2188ff 8px,
            transparent 8px,
            transparent 16px
        );
        margin-bottom: 25px;
    }

    .bot-message {
        background-color: #172438;
        border: 1px solid #263b55;
        border-radius: 18px;
        padding: 18px;
        margin: 12px 0;
        color: #eaf4ff;
    }

    .user-message {
        background-color: #1677ff;
        border-radius: 18px;
        padding: 18px;
        margin: 12px 0;
        color: white;
    }

    .agent-status {
        background-color: #101d2d;
        border: 1px solid #263b55;
        border-radius: 12px;
        padding: 12px;
        margin: 5px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="wanderly-title">✈️ Wanderly</div>
    <div class="wanderly-subtitle">AI Travel Planner</div>
    <div class="route"></div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ✈️ Plan Your Trip")

    current_location = st.text_input(
        "Current Location",
        placeholder="Example: Chennai"
    )

    destination = st.text_input(
        "Destination",
        placeholder="Example: Goa"
    )

    days = st.number_input(
        "Number of Days",
        min_value=1,
        max_value=30,
        value=3
    )

    budget = st.number_input(
        "Budget (₹)",
        min_value=1000,
        value=20000,
        step=1000
    )

    interests = st.text_input(
        "Interests",
        placeholder="Beach, food, adventure"
    )

    travel_dates = st.text_input(
        "Travel Dates",
        placeholder="Example: October 10-12"
    )

    travellers = st.number_input(
        "Travellers",
        min_value=1,
        max_value=20,
        value=2
    )

    st.markdown("---")

    plan_button = st.button(
        "✈️ Create Travel Plan",
        use_container_width=True
    )


# =========================================================
# QUICK CHIPS
# =========================================================

st.markdown("### Quick Planning")

col1, col2, col3 = st.columns(3)

with col1:
    st.button("💰 Budget", use_container_width=True)

with col2:
    st.button("🏨 Hotels", use_container_width=True)

with col3:
    st.button("🍴 Food", use_container_width=True)


# =========================================================
# WELCOME MESSAGE
# =========================================================

if not plan_button:

    st.markdown(
        """
        <div class="bot-message">
        ✈️ Hi! I'm Wanderly.<br><br>
        I can create a personalized travel plan using multiple AI agents.
        <br><br>
        Enter your trip details from the sidebar and click
        <b>Create Travel Plan</b>.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# START PLANNING
# =========================================================

if plan_button:

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if not current_location:
        st.warning("Please enter your current location.")
        st.stop()

    if not destination:
        st.warning("Please enter your destination.")
        st.stop()

    if not interests:
        interests = "General sightseeing"

    if not travel_dates:
        travel_dates = "Flexible dates"


    # -----------------------------------------------------
    # USER INPUT DISPLAY
    # -----------------------------------------------------

    st.markdown(
        f"""
        <div class="user-message">
        📍 <b>{current_location}</b> → <b>{destination}</b><br><br>
        🗓️ {days} days &nbsp;&nbsp;
        💰 ₹{budget} &nbsp;&nbsp;
        👥 {travellers} travellers<br><br>
        ❤️ Interests: {interests}
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # CREATE AGENTS
    # =====================================================

    with st.spinner("✈️ Starting Wanderly agents..."):

        try:

            manager = create_manager(llm)

            destination_agent = create_destination_agent(llm)
            itinerary_agent = create_itinerary_agent(llm)
            budget_agent = create_budget_agent(llm)
            weather_agent = create_weather_agent(llm)
            food_agent = create_food_agent(llm)
            transportation_agent = create_transportation_agent(llm)
            hotel_agent = create_hotel_agent(llm)
            interest_agent = create_interest_agent(llm)

        except Exception as e:

            st.error(
                f"Unable to create agents: {str(e)}"
            )
            st.stop()


    # =====================================================
    # TASK 1 - DESTINATION RESEARCH
    # =====================================================

    research_task = Task(
        description=f"""
        Research the destination: {destination}.

        Identify:
        - Famous tourist places
        - Major attractions
        - Popular hotspots
        - Important sightseeing locations
        - Places suitable for the user's interests

        User interests:
        {interests}

        Give concise and useful research.
        """,

        expected_output="""
        A concise list of important tourist places,
        attractions and hotspots.
        """,

        agent=destination_agent
    )


    # =====================================================
    # TASK 2 - INTEREST MATCHING
    # =====================================================

    interest_task = Task(
        description=f"""
        Match the traveler's interests with suitable
        activities and locations in {destination}.

        Traveler interests:
        {interests}

        Recommend the best matching activities.
        """,

        expected_output="""
        Personalized activities and places matching
        the traveler's interests.
        """,

        agent=interest_agent
    )


    # =====================================================
    # TASK 3 - TRANSPORTATION
    # =====================================================

    transportation_task = Task(
        description=f"""
        Plan transportation for the trip.

        Current location:
        {current_location}

        Destination:
        {destination}

        Recommend:
        - Best ways to travel from current location
          to destination
        - Local transportation options
        - Practical transportation suggestions
        """,

        expected_output="""
        Practical transportation recommendations
        for the trip.
        """,

        agent=transportation_agent
    )


    # =====================================================
    # TASK 4 - HOTEL
    # =====================================================

    hotel_task = Task(
        description=f"""
        Recommend suitable accommodation areas
        in {destination}.

        Travellers:
        {travellers}

        Total budget:
        ₹{budget}

        Recommend suitable hotel types and areas.
        Focus on practical and budget-conscious options.
        """,

        expected_output="""
        Suitable hotel areas and accommodation types.
        """,

        agent=hotel_agent
    )


    # =====================================================
    # TASK 5 - WEATHER
    # =====================================================

    weather_task = Task(
        description=f"""
        Provide weather-related travel guidance.

        Destination:
        {destination}

        Travel dates:
        {travel_dates}

        Explain:
        - Expected general weather conditions
        - Suitable activities
        - Things travelers should prepare
        """,

        expected_output="""
        Weather-related travel guidance and preparation tips.
        """,

        agent=weather_agent
    )


    # =====================================================
    # TASK 6 - FOOD
    # =====================================================

    food_task = Task(
        description=f"""
        Recommend local food in {destination}.

        Include:
        - Famous local dishes
        - Foods the traveler should try
        - Suitable restaurant areas
        - Food suggestions based on interests

        Interests:
        {interests}
        """,

        expected_output="""
        Local food, famous dishes and restaurant-area
        recommendations.
        """,

        agent=food_agent
    )


    # =====================================================
    # TASK 7 - BUDGET
    # =====================================================

    budget_task = Task(
        description=f"""
        Create an estimated travel budget.

        Current location:
        {current_location}

        Destination:
        {destination}

        Days:
        {days}

        Travellers:
        {travellers}

        Maximum budget:
        ₹{budget}

        Include estimated costs for:

        - Transportation
        - Hotel
        - Food
        - Activities

        Keep the estimated trip close to or below
        the user's stated budget.
        """,

        expected_output="""
        Category-wise estimated travel budget
        with total estimated cost.
        """,

        agent=budget_agent
    )


    # =====================================================
    # TASK 8 - ITINERARY
    # =====================================================

    itinerary_task = Task(
        description=f"""
        Create a day-by-day travel itinerary.

        Current location:
        {current_location}

        Destination:
        {destination}

        Days:
        {days}

        Travel dates:
        {travel_dates}

        Travellers:
        {travellers}

        Interests:
        {interests}

        Use the available destination research,
        interest recommendations, transportation,
        hotel, weather, food and budget information.

        Create:

        Day 1
        Day 2
        Day 3
        ...

        For each day include:
        - Morning
        - Afternoon
        - Evening
        - Food suggestion
        - Places to visit

        Make the itinerary practical.
        """,

        expected_output="""
        A complete day-by-day travel itinerary
        with activities and food suggestions.
        """,

        agent=itinerary_agent,

        context=[
            research_task,
            interest_task,
            transportation_task,
            hotel_task,
            weather_task,
            food_task,
            budget_task
        ]
    )


    # =====================================================
    # TASK 9 - MANAGER
    # =====================================================

    final_task = Task(
        description=f"""
        Create the final Wanderly travel plan.

        Trip:

        Current location:
        {current_location}

        Destination:
        {destination}

        Days:
        {days}

        Budget:
        ₹{budget}

        Travellers:
        {travellers}

        Interests:
        {interests}

        Travel dates:
        {travel_dates}

        Combine all available agent results.

        The final answer must contain:

        1. Trip Summary
        2. Transportation
        3. Hotel recommendation
        4. Day-by-day itinerary
        5. Food recommendations
        6. Weather guidance
        7. Estimated budget
        8. Interest-based activities
        9. Travel tips

        Make the final response clear and practical.

        Do not mention internal agents or CrewAI.
        """,

        expected_output="""
        A complete personalized travel plan
        formatted clearly for the traveler.
        """,

        agent=manager,

        context=[
            research_task,
            interest_task,
            transportation_task,
            hotel_task,
            weather_task,
            food_task,
            budget_task,
            itinerary_task
        ]
    )


    # =====================================================
    # CREW
    # =====================================================

    crew = Crew(
        agents=[
            manager,
            destination_agent,
            itinerary_agent,
            budget_agent,
            weather_agent,
            food_agent,
            transportation_agent,
            hotel_agent,
            interest_agent
        ],

        tasks=[
            research_task,
            interest_task,
            transportation_task,
            hotel_task,
            weather_task,
            food_task,
            budget_task,
            itinerary_task,
            final_task
        ],

        process=Process.sequential,

        verbose=False
    )


    # =====================================================
    # RUN CREW
    # =====================================================

    st.markdown("### ✈️ Wanderly is planning your trip...")

    progress = st.progress(0)

    try:

        progress.progress(20)

        result = crew.kickoff()

        progress.progress(100)

        st.markdown("### ✈️ Your Travel Plan")

        st.markdown(
            f"""
            <div class="bot-message">
            {result}
            </div>
            """,
            unsafe_allow_html=True
        )

    except Exception as e:

        progress.empty()

        st.error(
            f"Wanderly encountered an error: {str(e)}"
        )
