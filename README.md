# TripMates - Team Trip Planner AI Agent

## 🧩 The Challenge

Finding the perfect destination for a group of friends living in different locations can be challenging. We've built a smart travel planner that helps groups easily discover ideal destinations based on everyone's preferences, creating a fun, collaborative experience where every member has input in the final decision.

This project was created for the HackUPC 2025 challenge: **"The Perfect Reunion: Finding the Best Destination for Friends Around the World"**, by SkyScanner.

## ✨ Features

- **Real-time Voice Interaction**: Talk to our AI trip planner through an interactive interface
- **Collaborative Decision Making**: Input preferences from all group members to find the perfect destination
- **Built in Flight Search**: Integration with Skyscanner API to find the best flight options
- **Personalized Recommendations**: Get destination suggestions based on group interests and constraints
- **Real-time Animations**: Engaging interface with responsive visual feedback
- **Live Transcription**: See your conversation with the AI in real-time

## 📷 Screenshots

![App Screenshot 1](images/start-new-trip.png)

![App Screenshot 2](images/trip-planner-agent.png)

## 🔧 Tech Stack

- **Frontend**: React with LiveKit for real-time communication
- **Backend**: Python with LiveKit Agents
- **AI**: Custom agent built with LiveKit Agents framework
- **APIs**: Skyscanner for flight data, Deepgram for transcription, OpenAI for natural language processing

## 🚀 Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create `.env` file from the example:
   ```
   cp .env.example .env
   ```

4. Fill in the API keys in the `.env` file:
   ```
   LIVEKIT_API_KEY=<your_api_key>
   LIVEKIT_API_SECRET=<your_api_secret>
   LIVEKIT_URL=wss://<project-subdomain>.livekit.cloud
   DEEPGRAM_API_KEY=<your_deepgram_key>
   OPENAI_API_KEY=<your_openai_key>
   CARTESIA_API_KEY=<your_cartesia_key>
   SKYSCANNER_API_KEY=<your_skyscanner_key>
   SENDGRID_API_KEY=<your_sendgrid_key>
   ```

5. Run the server:
   ```
   python main.py dev
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create `.env` file from the example:
   ```
   cp .env.example .env
   ```

4. Fill in the API keys in the `.env` file:
   ```
   LIVEKIT_API_KEY=<your_api_key>
   LIVEKIT_API_SECRET=<your_api_secret>
   LIVEKIT_URL=wss://<project-subdomain>.livekit.cloud
   ```

5. Run the development server:
   ```
   npm run dev
   ```

## 🏗️ Architecture

The application consists of two main components:

1. **Python Backend**: 
   - Handles the AI agent logic with LiveKit Agents
   - Integrates with Skyscanner API for flight data
   - Processes user preferences and generates travel recommendations

2. **React Frontend**:
   - Provides an interactive voice interface
   - Displays real-time transcriptions and AI responses
   - Shows flight options and destination recommendations
   - Connects to backend via WebSockets for real-time communication