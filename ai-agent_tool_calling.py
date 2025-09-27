import gradio as gr
from dotenv import load_dotenv
from agents import Agent, Runner
from agents.tool import function_tool
from datetime import datetime
import random

load_dotenv(override=True)

ATTRACTIONS = {
    "luna_park": {"name": "Luna Park", "hours": {"weekday": "11:00 AM - 6:00 PM", "weekend": "11:00 AM - 10:00 PM"}, "price": 54, "location": "Milsons Point", "closure_dates": ["2025-11-01"]},
    "opera_house": {"name": "Sydney Opera House", "hours": {"daily": "9:00 AM - 8:30 PM"}, "price": 42, "location": "Circular Quay"},
    "harbour_bridge": {"name": "Sydney Harbour Bridge", "hours": {"daily": "24/7"}, "price": 0, "location": "The Rocks", "note": "Free to walk across, BridgeClimb tours available"},
    "bondi_beach": {"name": "Bondi Beach", "hours": {"daily": "24/7"}, "price": 0, "location": "Bondi", "note": "Free public beach, famous for surfing and coastal walk"}
}

@function_tool
def get_weather(date_str: str) -> str:
    """Get weather for Sydney on a specific date (YYYY-MM-DD format)."""
    try:
        month = datetime.strptime(date_str, "%Y-%m-%d").month
        if month in [12, 1, 2]: temp_range, conditions = (20, 30), ["Sunny", "Partly Cloudy", "Showers"]
        elif month in [6, 7, 8]: temp_range, conditions = (8, 17), ["Mild", "Cool", "Rain"]
        else: temp_range, conditions = (15, 25), ["Mild", "Pleasant", "Partly Cloudy"]
        
        return f"Weather for {date_str}: {random.uniform(*temp_range):.1f}°C, {random.choice(conditions)}"
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD"

@function_tool
def get_attractions_info(attraction: str = None) -> str:
    """Get information about Sydney attractions."""
    if attraction:
        key = attraction.lower().replace(" ", "_")  # normalize
        if key in ATTRACTIONS:
            attr = ATTRACTIONS[key]
            return f"{attr['name']} - Price: AUD {attr['price']}, Location: {attr['location']}"
        else:
            # Return all attractions as suggestions when not found
            suggestions = "\n".join(
                f"{attr['name']} - Price: AUD {attr['price']}, Location: {attr['location']}"
                for attr in ATTRACTIONS.values()
            )
            return f"Sorry, I couldn't find '{attraction}'. Here are some options you might like:\n{suggestions}"
    
    # Return all attractions info when no specific attraction requested
    return "\n".join(
        f"{attr['name']} - Price: AUD {attr['price']}, Location: {attr['location']}"
        for attr in ATTRACTIONS.values()
    )


# Create agent and UI
agent = Agent(
    name="QA Agent",
    instructions="You are a helpful assistant. Answer questions briefly, use tools to get accurate information.",
    model="gpt-3.5-turbo",
    tools=[get_weather, get_attractions_info],
)

async def chat_with_agent(message, history):
    return (await Runner.run(agent, message)).final_output

# Launch Gradio interface
gr.ChatInterface(
    fn=chat_with_agent,
    title="AI Assistant with Tools",
    description="Ask me anything and I'll help you out!",
    theme="soft"
).launch()