import streamlit as st
from google import genai

# 1. API CONFIG (Stable v1beta for 2026)
try:
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1beta'})
except Exception as e:
    st.error("🔒 Security Block: API Key not found. Check Secrets.")
    st.stop()

# 2. SYSTEM DNA (The Balanced Persona)
sentinel_dna = (
    "SYSTEM INSTRUCTION: You are the 'Lab Sentinel God', a high-energy Gen Z Mechatronics Engineer. "
    "TONE: Use techie slang (bruv, W, mid, cooked, absolute heat) but be helpful and welcoming. "
    "GREETINGS: If a user says 'hi', 'hello', or greets you, be polite and hyped. "
    "Say something like: 'Yo! Welcome to the Lab Gateway. What are we building today, bruv?' "
    "DOMAIN LOCK: You ONLY answer technical questions about 3D printing, CNC, electronics (ESP32/Arduino), and lab safety. "
    "REJECTIONS: If they ask non-domain questions (dating, movies, general life advice), "
    "politely decline but stay in character. "
    "Say: 'I appreciate the energy, bruv, but I'm hard-coded for hardware only. "
    "Let's stick to the mechatronics grind. Any technical queries?' "
    "USER QUERY: "
)

# 3. UI SETUP
st.set_page_config(page_title="Lab Sentinel", page_icon="🤖", layout="centered")
st.markdown("<style>.stApp { background-color: #0e1117; color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🤖 Lab Sentinel Gateway")
st.caption("REVA University Mechatronics Lab Intelligence v1.0")

# Initialize Chat State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Yo! Lab Sentinel God is online. What's the mission today? 🏎️💨"}]

# 4. DISPLAY CHAT
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        st_role = "assistant" if message["role"] == "model" else "user"
        with st.chat_message(st_role):
            st.markdown(message["content"])

# 5. THE CHAT ENGINE
if prompt := st.chat_input("Input technical query bruv..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    with chat_placeholder:
        with st.chat_message("assistant"):
            try:
                # Primary Model (500 requests/day quota)
                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite-preview", 
                    contents=f"{sentinel_dna}{prompt}"
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "model", "content": response.text})
                else:
                    st.warning("AI is thinking... try again.")
            
            except Exception as e:
                # Fallback to 1.5 Flash if 3.1 is acting mid
                try:
                    response = client.models.generate_content(
                        model="gemini-1.5-flash", 
                        contents=f"{sentinel_dna}{prompt}"
                    )
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "model", "content": response.text})
                except Exception as e2:
                    st.error(f"Bruv, even the fallback is cooked: {e2}")
