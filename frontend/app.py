import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="centered"  # Changed from "wide" to "centered" for single column layout
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'travel_plan' not in st.session_state:
    st.session_state.travel_plan = None

# Function to change pages
def change_page(page):
    st.session_state.page = page

# Function to simulate the AI agent response (replace with actual API call)
def get_ai_travel_plan(preferences):
    """
    This is a placeholder function. Replace with your actual AI agent API call.
    """
    # This would be replaced with your actual AI agent that calls Skyscanner API
    return {
        "destination": preferences["destination"] if preferences["destination"] else "Paris, France",
        "dates": f"{preferences['departure_date']} to {preferences['return_date']}",
        "flights": {
            "outbound": {
                "departure": f"{preferences['origin']} - {preferences['departure_date']} 10:00",
                "arrival": f"Paris, France - {preferences['departure_date']} 12:30",
                "airline": "Air France",
                "price": "€120"
            },
            "return": {
                "departure": f"Paris, France - {preferences['return_date']} 14:00",
                "arrival": f"{preferences['origin']} - {preferences['return_date']} 16:30",
                "airline": "Air France",
                "price": "€130"
            },
            "total_price": "€250 per person"
        },
        "accommodation": {
            "name": "Hotel de Paris",
            "location": "Central Paris",
            "price": f"€{95 * (preferences['return_date'] - preferences['departure_date']).days} total"
        },
        "itinerary": [
            {"day": 1, "activities": ["Eiffel Tower", "Seine River Cruise", "Dinner at a local bistro"]},
            {"day": 2, "activities": ["Louvre Museum", "Champs-Élysées shopping", "Fine dining experience"]},
            {"day": 3, "activities": ["Notre Dame Cathedral", "Latin Quarter exploration", "Evening show"]}
        ],
        "estimated_total_cost": f"€{min(preferences['budget'], 850)} per person"
    }

# Handle form submission
def handle_form_submit():
    with st.spinner("AI is creating your perfect travel plan..."):
        # Collect form data
        preferences = {
            "origin": st.session_state.origin,
            "destination": st.session_state.destination,
            "departure_date": st.session_state.departure_date,
            "return_date": st.session_state.return_date,
            "budget": st.session_state.budget,
            "trip_type": st.session_state.trip_type,
            "travelers": st.session_state.travelers,
            "additional_prefs": st.session_state.additional_prefs
        }
        
        # Get AI-generated travel plan
        travel_plan = get_ai_travel_plan(preferences)
        
        # Store in session state
        st.session_state.travel_plan = travel_plan
        st.session_state.preferences = preferences
        
        # Change page
        change_page('results')

# App title and description - appears on all pages
st.title("✈️ AI Travel Planner")

# INPUT PAGE
if st.session_state.page == 'input':
    st.subheader("Let AI create your perfect travel itinerary")
    
    # Create a form for user preferences
    with st.form(key="travel_preferences"):
        # Origin and destination - now in single column
        st.text_input("Departure City", "Barcelona", key="origin")
        st.text_input("Destination (city, country, or 'anywhere')", "", key="destination")
        
        # Date selection
        today = datetime.today()
        tomorrow = today + timedelta(days=1)
        next_week = today + timedelta(days=7)
        
        st.date_input("Departure Date", tomorrow, key="departure_date")
        st.date_input("Return Date", next_week, key="return_date")
        
        # Budget
        st.slider("Budget (€)", 200, 5000, 1000, 100, key="budget")
        
        # Trip type
        st.selectbox(
            "Trip Type",
            ["Beach", "City Break", "Adventure", "Cultural", "Relaxation", "Any"],
            key="trip_type"
        )
        
        # Number of travelers
        st.number_input("Number of Travelers", 1, 10, 1, key="travelers")
        
        # Additional preferences
        st.text_area("Additional Preferences (optional)", 
                     "e.g. vegetarian food, accessibility needs, etc.",
                     key="additional_prefs")
        
        # Submit button
        st.form_submit_button(label="Generate Travel Plan", on_click=handle_form_submit)

# RESULTS PAGE
elif st.session_state.page == 'results':
    travel_plan = st.session_state.travel_plan
    preferences = st.session_state.preferences
    
    # Back button
    st.button("← Back to Preferences", on_click=lambda: change_page('input'))
    
    st.success("Your travel plan is ready!")
    
    # Overview section - now in single column
    st.header(f"Your Trip to {travel_plan['destination']}")
    st.subheader(f"📅 {travel_plan['dates']}")
    
    st.metric("Estimated Cost", travel_plan['estimated_total_cost'])
    st.metric("Trip Duration", f"{(preferences['return_date'] - preferences['departure_date']).days} days")
    
    st.info(f"This trip plan was tailored for {preferences['travelers']} traveler(s) seeking a {preferences['trip_type'].lower()} experience.")
    
    # Create tabs for organized display
    tab1, tab2, tab3 = st.tabs(["Overview", "Flights & Accommodation", "Itinerary"])
    
    with tab1:
        # Overview summary - redundant information is displayed here
        st.subheader("Trip Summary")
        st.write(f"Destination: {travel_plan['destination']}")
        st.write(f"Dates: {travel_plan['dates']}")
        st.write(f"Total Estimated Cost: {travel_plan['estimated_total_cost']}")
    
    with tab2:
        st.subheader("✈️ Flight Details")
        
        # Outbound flight
        st.markdown("**Outbound Flight**")
        st.markdown(f"From: {travel_plan['flights']['outbound']['departure']}")
        st.markdown(f"To: {travel_plan['flights']['outbound']['arrival']}")
        st.markdown(f"Airline: {travel_plan['flights']['outbound']['airline']}")
        st.markdown(f"Price: {travel_plan['flights']['outbound']['price']}")
        
        # Return flight
        st.markdown("**Return Flight**")
        st.markdown(f"From: {travel_plan['flights']['return']['departure']}")
        st.markdown(f"To: {travel_plan['flights']['return']['arrival']}")
        st.markdown(f"Airline: {travel_plan['flights']['return']['airline']}")
        st.markdown(f"Price: {travel_plan['flights']['return']['price']}")
        
        st.markdown(f"**Total Flight Cost:** {travel_plan['flights']['total_price']}")
        
        # Accommodation
        st.subheader("🏨 Accommodation")
        st.markdown(f"**{travel_plan['accommodation']['name']}**")
        st.markdown(f"Location: {travel_plan['accommodation']['location']}")
        st.markdown(f"Price: {travel_plan['accommodation']['price']}")
    
    with tab3:
        st.subheader("📝 Itinerary")
        
        for day in travel_plan['itinerary']:
            with st.expander(f"Day {day['day']}"):
                for activity in day['activities']:
                    st.markdown(f"- {activity}")
    
    # Add a download button for the travel plan
    st.download_button(
        label="Download Travel Plan",
        data=json.dumps(travel_plan, indent=4),
        file_name="travel_plan.json",
        mime="application/json"
    )
    
    # Plan another trip button
    st.button("Plan Another Trip", on_click=lambda: change_page('input'))

# Add a footer
st.markdown("---")
st.markdown("*Powered by AI and Skyscanner API*")

