import streamlit as st
import pymysql
import google.generativeai as genai
from googleapiclient.discovery import build
import asyncio

st.set_page_config(
    page_title="LevelUP",
    page_icon="logo.png",
    layout="wide"
)

# Load secrets
GENAI_API_KEY = st.secrets["AIzaSyD8dYmlfLDp9xV2EUSWRf_zkiwqmusSLMg"]["genai"]
YOUTUBE_API_KEY = st.secrets["AIzaSyDo5jkE6EHySmkx6wqDPV1w1KZ5JrEkG7s"]["youtube"]
DB_CONFIG = st.secrets["roadmap_db"]

# Configure Gemini AI
genai.configure(api_key=GENAI_API_KEY)

def connect_to_db():
    return pymysql.connect(
        host=DB_CONFIG["localhost"],
        user=DB_CONFIG["root"],
        password=DB_CONFIG["mysql#7V"],
        database=DB_CONFIG["roadmap_db"],
        cursorclass=pymysql.cursors.DictCursor
    )

async def generate_job_roles(domain):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Generate a list of job roles for the domain: {domain}. Provide at least 10 job roles."
        response = model.generate_content(prompt)
        job_roles = response.text.split('\n') if response.text else ["No job roles found"]
        return [role.split('-')[0].strip() for role in job_roles]
    except Exception as e:
        return [f"Error: {e}"]

def fetch_youtube_playlists(job_role):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY, cache_discovery=False)
    request = youtube.search().list(q=job_role + " tutorial", part='snippet', type='playlist', maxResults=9)
    response = request.execute()
    return [{"title": item['snippet']['title'], "url": f"https://www.youtube.com/playlist?list={item['id']['playlistId']}", "thumbnail": item['snippet']['thumbnails']['high']['url']} for item in response['items']]

async def generate_roadmap(job_role, skill_level):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Generate a structured 30-day learning roadmap for someone starting as a {job_role} with a {skill_level} skill level."
        response = model.generate_content(prompt)
        return response.text if response.text else "No roadmap found"
    except Exception as e:
        return f"Error: {e}"

async def handle_find_job_roles():
    if domain:
        with st.spinner("Fetching job roles..."):
            job_roles = await generate_job_roles(domain)
        st.session_state['job_roles'] = job_roles
        st.success("Job Roles Generated! Select one below.")
    else:
        st.error("Please enter your domain")

# Streamlit UI
st.title("Unlock Your Potential, One Skill at a Time! ✨")
domain = st.sidebar.selectbox("Select Your Domain:", ["Data Science", "Web Development", "Cyber Security", "IoT", "Cloud Computing", "AI"])

if st.sidebar.button("Find Job Roles"):
    asyncio.run(handle_find_job_roles())

if "job_roles" in st.session_state:
    selected_job_role = st.selectbox("Select a Job Role:", st.session_state['job_roles'])
    skill_level = st.selectbox("Select your skill level:", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("Generate Roadmap"):
        with st.spinner("Generating roadmap..."):
            roadmap = asyncio.run(generate_roadmap(selected_job_role, skill_level))
        st.write("## 🚀 30-Day Roadmap:")
        st.markdown(roadmap)
    
    if st.button("Find Resources"):
        with st.spinner("Fetching YouTube resources..."):
            playlists = fetch_youtube_playlists(selected_job_role)
        for playlist in playlists:
            st.markdown(f"[![{playlist['title']}]({playlist['thumbnail']})]({playlist['url']})")
