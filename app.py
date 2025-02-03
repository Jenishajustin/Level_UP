import streamlit as st
import pymysql
import google.generativeai as genai
from googleapiclient.discovery import build
import os
import time
import asyncio

st.set_page_config(
    page_title="LevelUP",
    page_icon="logo.png",  # Specify the path to your PNG logo
    layout="wide"
)

# Custom CSS for sidebar styling
st.markdown("""
    <style>
        /* Center the image at the top of the sidebar */
        .css-1d391kg {
            display: flex;
            justify-content: center;
            padding-top: 0px;
        }
        
        /* Reduce spacing between the logo and the 'Enter Your Details' section */
        .css-16cvyrg {
            padding-top: 0rem !important;
        }

        /* Adjust the size of the image */
        .css-1d391kg img {
            max-width: 100%;
            height: auto;
        }
    </style>
""", unsafe_allow_html=True)

# Load and display the logo in the sidebar
logo_path = "levelup_logo.png"  # Specify the path to your logo
st.sidebar.image(logo_path, use_container_width=True)

# Streamlit UI
st.title("Unlock Your Potential, One Skill at a Time! ✨")

# Step 1: User inputs domain & skills
st.sidebar.header("Enter Your Details")
domain = st.sidebar.selectbox("Select Your Domain:", ["Data Science", "Web Development", "Cyber Security", "Internet of Things (IoT)", "Cloud Computing", "Artificial Intelligence (AI)"])


# Set your Gemini AI API Key
genai.configure(api_key="AIzaSyD8dYmlfLDp9xV2EUSWRf_zkiwqmusSLMg")  # Replace with your actual API key

# Database connection function
def connect_to_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="mysql#7V",
        database="roadmap_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# Function to get job roles dynamically from Gemini AI based on domain
async def generate_job_roles(domain):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Generate a list of job roles for the domain: {domain}. Provide at least 10 job roles."
        response = model.generate_content(prompt)
        
        # Assuming the response text contains job roles separated by newlines
        job_roles = response.text.split('\n') if response.text else ["No job roles found"]
        
        # Clean the job roles by keeping only the job role names and removing descriptions
        job_roles = [role.split('-')[0].strip() for role in job_roles]  # Split by '-' to remove description if present
        
        return job_roles
    except Exception as e:
        return [f"Error: {e}"]

# Fetch YouTube playlists with job role-based filtering
def fetch_youtube_playlists(job_role):
    api_key = "AIzaSyDo5jkE6EHySmkx6wqDPV1w1KZ5JrEkG7s"
    youtube = build('youtube', 'v3', developerKey=api_key, cache_discovery=False)

    request = youtube.search().list(
        q=job_role + " tutorial",
        part='snippet',
        type='playlist',
        maxResults=9  # Fetch 9 playlists for a 3x3 grid
    )
    response = request.execute()
    
    playlists = []
    for item in response['items']:
        playlists.append({
            "title": item['snippet']['title'],
            "url": f"https://www.youtube.com/playlist?list={item['id']['playlistId']}",
            "thumbnail": item['snippet']['thumbnails']['high']['url']
        })
    
    return playlists
# Function to generate a roadmap based on the job role and skill level
async def generate_roadmap(job_role, skill_level):
    try:
        model = genai.GenerativeModel("gemini-pro")
        # Adjust the prompt based on the job role and skill level
        prompt = f"Generate a structured 30-day learning roadmap for someone starting as a {job_role} with a {skill_level} skill level. Provide the roadmap from beginner to advanced level."
        response = model.generate_content(prompt)
        
        return response.text if response.text else "No roadmap found"
    except Exception as e:
        return f"Error: {e}"

async def handle_find_job_roles():
    if domain:
        with st.spinner("Fetching job roles..."):
            job_roles = await generate_job_roles(domain)
        st.session_state['job_roles'] = job_roles
        st.session_state['selected_domain'] = domain
        st.session_state['generated_roadmap'] = ""  # Clear previous roadmap
        st.session_state['playlists'] = []  # Clear previous playlists
        st.session_state['resources_shown'] = False  # Reset resources flag
        st.session_state['roadmap_shown'] = False  # Reset roadmap flag
        st.success("Job Roles Generated! Select one below.")
    else:
        st.error("Please enter your domain")

if st.sidebar.button("Find Job Roles"):
    asyncio.run(handle_find_job_roles())

# Step 2: User selects a job role
if "job_roles" in st.session_state and 'selected_domain' in st.session_state:
    selected_job_role = st.selectbox("Select a Job Role:", st.session_state['job_roles'], key="job_role_selector")
    skill_level = st.selectbox("Select your skill level:", ["Beginner", "Intermediate", "Advanced"], key="skill_level_selector")
    
    # Generate roadmap if new skill level or job role is selected
    if st.button("Generate Roadmap") and not st.session_state['roadmap_shown']:
        with st.spinner("Generating roadmap..."):
            roadmap = asyncio.run(generate_roadmap(selected_job_role, skill_level))
        st.session_state['generated_roadmap'] = roadmap
        st.session_state['roadmap_shown'] = True  # Mark roadmap as shown

    # Display the roadmap if already generated
    if 'generated_roadmap' in st.session_state and st.session_state['roadmap_shown']:
        st.write("## 🚀 30-Day Roadmap:")
        st.markdown(f"**{selected_job_role} ({skill_level} level)**: \n {st.session_state['generated_roadmap']}")
    
    # Fetch resources for selected job role
    if st.button("Find Resources") and not st.session_state['resources_shown']:
        with st.spinner("Fetching YouTube resources..."):
            playlists = fetch_youtube_playlists(selected_job_role)
        st.session_state['playlists'] = playlists
        st.session_state['resources_shown'] = True  # Mark resources as shown

    # Display resources if already fetched
    if 'playlists' in st.session_state and st.session_state['resources_shown']:
        st.write("## 📺 Recommended YouTube Playlists:")

        playlists = st.session_state['playlists']
        num_columns = 3  
        num_rows = len(playlists) // num_columns + (1 if len(playlists) % num_columns != 0 else 0)
        
        for row in range(num_rows):
            cols = st.columns(num_columns)  
            
            for col in range(num_columns):
                playlist_index = row * num_columns + col
                if playlist_index < len(playlists):
                    playlist = playlists[playlist_index]
                    with cols[col]:
                        st.markdown(f"""
                        <div style="border: 2px solid #ccc; border-radius: 8px; padding: 10px; text-align: center; margin: 10px;">
                            <a href="{playlist['url']}" target="_blank">
                                <img src="{playlist['thumbnail']}" alt="{playlist['title']}" width="250" height="160">
                                <div><strong>{playlist['title']}</strong></div>
                            </a>
                        </div>
                        """, unsafe_allow_html=True)

# Chatbot Section (Enhanced Gemini-like Interface)
st.subheader("💬 Hey there! I'm Nano, your career buddy!")

# Function to get chatbot response using Gemini AI
async def get_gemini_response(user_input):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)
        return response.text if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"Error: {e}"

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input for chatbot
user_input = st.chat_input("Ask away, I'm all ears!")

async def handle_user_input(user_input):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get chatbot response asynchronously
    with st.spinner("Getting response..."):
        bot_response = await get_gemini_response(user_input)
    
    # Add bot message to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display user and bot messages
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        st.markdown(bot_response)

if user_input:
    asyncio.run(handle_user_input(user_input))

