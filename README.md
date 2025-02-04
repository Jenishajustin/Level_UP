# LevelUP: AI-Powered Skill Development & Learning Platform  

LevelUP is an AI-driven platform that helps individuals find **suitable job roles, generate structured learning roadmaps, and access curated learning resources**. Built using **Streamlit, Google Gemini AI, YouTube API, and MySQL**, it simplifies career planning by offering **personalized recommendations** and an **AI-powered chatbot (Nano)** for guidance.  

---

## Features  

### 1. **Personalized Career Roadmap Generator**  
🔹 Users **select a domain** (e.g., Data Science, Web Development, AI, Cybersecurity).  
🔹 **Google Gemini AI suggests job roles** based on the selected domain.  
🔹 Users **choose a job role & skill level** (Beginner, Intermediate, Advanced).  
🔹 A **30-day structured learning roadmap** is generated dynamically.  

### 2. **Curated Learning Resources**  
🔹 The **YouTube API fetches recommended videos** for the chosen job role.  
🔹 Learning resources are displayed in a **3x3 grid format** for easy access.  

### 3. **AI-Powered Chatbot (Nano)**  
🔹 Built using **Google Gemini AI**, Nano assists users with **career advice, skill recommendations, and industry insights**.  
🔹 Users can **chat with Nano** to get real-time guidance.  

### 4. **MySQL Database Integration**  
🔹 Stores **user selections, progress, and roadmap details**.  
🔹 Ensures **efficient and scalable data management**.  

### 5. **Modern UI with Streamlit**  
🔹 **Sidebar for navigation & domain selection**.  
🔹 **Grid-based UI for job roles, roadmaps, and resources**.  
🔹 **Custom CSS styling** for a professional look.  

---

## Tech Stack  

| **Technology** | **Usage** |
|--------------|------------|
| **Python** | Backend logic & AI interactions |
| **Streamlit** | Frontend UI & user interaction |
| **Google Gemini AI** | Job role recommendations & chatbot |
| **YouTube API** | Fetching video playlists |
| **MySQL (pymysql)** | Storing user data & roadmaps |
| **Asyncio** | Handling asynchronous AI calls |

---

## How It Works?  

1️⃣ **User selects a domain** (e.g., AI, Web Development, Cloud Computing).  
2️⃣ **AI generates a list of job roles** related to the domain.  
3️⃣ **User selects a job role & skill level** (Beginner, Intermediate, Advanced).  
4️⃣ **A 30-day roadmap is generated** dynamically using Google Gemini AI.  
5️⃣ **YouTube API fetches learning resources** related to the job role.  
6️⃣ **Users can chat with Nano**, an AI chatbot for career guidance.  

---

## Future Enhancements  

🔹 **User authentication system** to save progress.  
🔹 **Gamification features** (progress tracking, achievement badges).  
🔹 **Integration with job portals** for real-world opportunities.  
🔹 **Mentor connect feature** to get guidance from industry professionals.  

---

## Installation & Setup  

1️⃣ **Clone the repository:**  
```bash
git clone https://github.com/your-username/LevelUP.git
cd LevelUP
```
2️⃣ **Install dependencies:** 
```bash
pip install -r requirements.txt
```
3️⃣ **Run the application:**

```bash
streamlit run app.py
```

---

## License
This project is licensed under the MIT License – feel free to modify and use it as needed!
