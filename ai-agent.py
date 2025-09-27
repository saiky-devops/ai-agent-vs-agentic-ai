import os
import gradio as gr
from dotenv import load_dotenv
from agents import Agent, Runner

# Make sure you set your API key
load_dotenv(override=True)
openai_api_key = os.getenv("OPENAI_API_KEY")

# Define a very simple Q/A agent
agent = Agent(
    name="QA Agent",
    instructions="You are a helpful assistant. Answer the user's questions briefly and clearly.",
    model="gpt-3.5-turbo"
)
# Function to handle chat
async def chat_with_agent(message, history):
    return (await Runner.run(agent, message)).final_output

# Build chat-like Gradio UI
demo = gr.ChatInterface(
    fn=chat_with_agent,
    title="AI Assistant (Traditional)",
    description="Ask me anything and I'll help you out!",
    theme="soft"
)

demo.launch()