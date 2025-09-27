import os
import random
from datetime import datetime
from dotenv import load_dotenv
import gradio as gr

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType

load_dotenv(override=True)

# -------------------------------
# Attractions Data
# -------------------------------
ATTRACTIONS = {
    "luna_park": {"name": "Luna Park", "closed": "2025-11-01", "price": 54, "location": "Milsons Point"},
    "opera_house": {"name": "Opera House", "closed": None, "price": 42, "location": "Circular Quay"},
    "harbour_bridge": {"name": "Sydney Harbour Bridge", "closed": None, "price": 0, "location": "The Rocks", "note": "Free to walk across, BridgeClimb tours available"},
    "bondi_beach": {"name": "Bondi Beach", "closed": None, "price": 0, "location": "Bondi", "note": "Free public beach, famous for surfing and coastal walk"}   
}

# -------------------------------
# Tools
# -------------------------------
def check_attraction(attraction_and_date: str) -> str:
    """Check attraction + find alternative if closed."""
    input_clean = attraction_and_date.strip().strip("'\"")
    parts = [p.strip().strip("'\"") for p in input_clean.split(",")]
    attraction = parts[0].lower().replace(" ", "_")
    date = parts[1] if len(parts) > 1 else None

    if attraction not in ATTRACTIONS:
        available = ", ".join(ATTRACTIONS.keys())
        return f"❌ '{attraction}' not found. Available: {available}"

    info = ATTRACTIONS[attraction]
    if date == info.get("closed"):
        alternatives = [n for n, d in ATTRACTIONS.items() if n != attraction and d["closed"] != date]
        if alternatives:
            alt = ATTRACTIONS[alternatives[0]]
            return f"🚫 {info['name']} closed on {date}.\n🔄 Alternative: {alt['name']} (${alt['price']} at {alt['location']})"
    return f"✅ {info['name']} is open - Price: AUD ${info['price']}, Location: {info['location']}"

def get_weather(date_str: str) -> str:
    """Return mock Sydney weather for date YYYY-MM-DD."""
    date_clean = date_str.strip().strip("'\"")
    try:
        month = datetime.strptime(date_clean, "%Y-%m-%d").month
        if month in [12, 1, 2]:
            temp_range, conditions = (20, 30), ["Sunny", "Partly Cloudy", "Showers"]
        elif month in [6, 7, 8]:
            temp_range, conditions = (8, 17), ["Mild", "Cool", "Rain"]
        else:
            temp_range, conditions = (15, 25), ["Mild", "Pleasant", "Partly Cloudy"]
        return f"🌤️ {date_clean}: {random.uniform(*temp_range):.1f}°C, {random.choice(conditions)}"
    except ValueError:
        return f"❌ Invalid date '{date_clean}'. Use YYYY-MM-DD."

# --- New tool to list all attractions ---
def list_attractions() -> str:
    """Return all attractions in Sydney."""
    return ", ".join(attr["name"] for attr in ATTRACTIONS.values())

tools = [
    Tool(name="CheckAttraction", func=check_attraction,
         description="Check if an attraction is open. Input format: 'luna_park, 2025-11-03'"),
    Tool(name="GetWeather", func=get_weather,
         description="Get Sydney weather. Input format: '2025-11-03'"),
    Tool(name="ListAttractions", func=list_attractions,
         description="List all verified attractions available in Sydney")
]

# -------------------------------
# LLM + Agent
# -------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=20,
    handle_parsing_errors=True,
    early_stopping_method="generate",
)

# -------------------------------
# Chat wrapper
# -------------------------------
def chat_with_agent(message, history):
    system_prompt = """
    You are a Sydney trip planner.
    Instructions:
    1. Use ListAttractions to see all verified attractions.
    2. Use CheckAttraction to check availability for specific dates.
    3. Use GetWeather to check weather.
    4. Suggest alternatives if attractions are closed or if weather is bad.
    5. Plan multi-day itineraries and avoid repeating the same attraction on consecutive days.
    6. Provide prices, locations, and notes if available.
    """
    try:
        response = agent.invoke({"input": f"{system_prompt}\nUser: {message}"})
        return response["output"]
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# -------------------------------
# Gradio UI
# -------------------------------
gr.ChatInterface(
    fn=chat_with_agent,
    title="AI Assistant with Agentic capabilities",
    description="Ask me anything about Sydney attractions and I'll help you out!",
    theme="soft",
).launch()