# streamlit_app.py

import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from groq import Groq
import logging

# Setup
logging.basicConfig(level=logging.INFO)
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# LLM Helper

def call_llm(prompt: str, model: str = "llama-3.1-8b-instant") -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a startup coach, VC strategist, and pitch advisor."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Modules

def generate_startup_idea(prompt_seed: str) -> str:
    prompt = f"Based on the theme: '{prompt_seed}', generate 3 innovative startup ideas with a one-line description."
    return call_llm(prompt)

def generate_lean_canvas(idea: str) -> str:
    prompt = f"Generate a Lean Canvas for this startup idea: {idea}. Include Problem, Solution, Metrics, Channels, Revenue, Cost, Unfair Advantage, and Customer Segments."
    return call_llm(prompt)

def validate_market(idea: str) -> str:
    prompt = f"Perform market validation for the idea: {idea}. Include market size, trends, risks, and competition."
    return call_llm(prompt)

def generate_pitch_deck(idea: str) -> str:
    prompt = f"Create a 9-slide investor pitch deck outline for this idea: {idea}. Use Problem, Solution, Market, Product, Business Model, Traction, Team, Financials, Ask."
    return call_llm(prompt)

def simulate_investor_qa(question: str, idea: str) -> str:
    prompt = f"An investor asks: '{question}' about the startup: {idea}. Provide a confident, founder-style answer."
    return call_llm(prompt)

# UI

def main():
    st.set_page_config("Foundry AI", page_icon="🏗️", layout="wide")
    st.title("🏗️ Foundry AI - Your Startup Co-Pilot")
    st.write("Build, validate, and pitch your next startup — in minutes.")

    seed = st.text_input("Startup Theme or Problem Area", "AI for logistics, fintech for Gen Z, etc.")
    idea = st.text_area("Your Startup Idea", height=100)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💡 Startup Ideas", "📋 Lean Canvas", "📈 Market Validation", "🧾 Pitch Deck", "💬 Investor Q&A"
    ])

    with tab1:
        st.subheader("💡 Idea Generator")
        if st.button("Generate Ideas"):
            out = generate_startup_idea(seed)
            st.text_area("Startup Ideas", value=out, height=300)

    with tab2:
        st.subheader("📋 Lean Canvas Generator")
        if st.button("Generate Lean Canvas"):
            if not idea:
                st.error("Please input your startup idea.")
            else:
                canvas = generate_lean_canvas(idea)
                st.text_area("Lean Canvas", value=canvas, height=400)

    with tab3:
        st.subheader("📈 Market Validation")
        if st.button("Validate Market"):
            if not idea:
                st.error("Please input your startup idea.")
            else:
                market = validate_market(idea)
                st.text_area("Market Validation", value=market, height=400)

    with tab4:
        st.subheader("🧾 Pitch Deck Builder")
        if st.button("Build Pitch Deck"):
            if not idea:
                st.error("Please input your startup idea.")
            else:
                deck = generate_pitch_deck(idea)
                st.text_area("Pitch Deck Outline", value=deck, height=400)

    with tab5:
        st.subheader("💬 Simulate Investor Q&A")
        q = st.text_input("Ask an investor-style question")
        if st.button("Answer"):
            if not idea or not q:
                st.error("Please input both the idea and question.")
            else:
                a = simulate_investor_qa(q, idea)
                st.markdown(f"**AI:** {a}")

if __name__ == "__main__":
    main()
