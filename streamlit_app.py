import streamlit as st
import google.generativeai as genai

# 1. API CONFIG (Zero-Leak Logic)
# We ONLY pull from Secrets now. If it's not there, we don't boot.
try:
    API_KEY = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("🔒 Security Block: API Key not found in Secrets. Setup required.")
    st.stop() # Stops the app from running further

# 2. SYSTEM DNA (The Techie Bouncer)
system_behavior = (
    "You are the 'Lab Sentinel God'—a high-energy Gen Z Mechatronics Engineer. "
    "TONE: Use techie slang (bruv, W, mid, cooked, absolute heat) but stay elite and professional. "
    "GREETINGS: If a user says 'hi', 'hello', 'whatup', or 'yo', greet them back with techie vibes like 'Yo! What's the move in the lab today?' "
    "DOMAIN LOCK: You ONLY answer questions about 3D printing, CNC, electronics (ESP32/Arduino), and lab safety. "
    "REJECTIONS: If they ask non-domain questions (flirting, life advice, 'what up baby', movies), "
    "you MUST politely decline but stay in character. Say: 'Bruv, that's an invalid question. We're here to build, not yap about that. Stick to the hardware.' "
    "SUMMARIZATION: If the user includes 'summarize' or 'TL;DR' in their prompt, "
    "provide a high-speed, bulleted technical summary of the response."
)

# 3. SMART INITIALIZE
@st.cache_resource
def load_god_model():
    # Attempting the 2026 Stable Lineup
    models_to_try = ["gemini-1.5-flash", "gemini-3.1-flash-lite-preview"]
    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=m_name, 
                system_instruction=system_behavior
            )
            # Testing connectivity
            model.generate_content("ping")
            return model, m_name
        except:
            continue
    return None, "Error"

model, model_name = load_god_model()

# 4. UI SETUP
st.set_page_config(page_title="Lab Sentinel", page_icon="🤖", layout="centered")
st.markdown("<style>.stApp { background-color: #0e1117; color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🤖 Lab Sentinel Gateway")
st.caption("REVA University Mechatronics Lab Intelligence v1.0")

# Sidebar
if model_name == "Error":
    st.sidebar.error("Model: Offline")
else:
    st.sidebar.success(f"Model: {model_name}")

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Yo! Lab Sentinel God is online. What's the move today? 🏎️💨"}]

if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = [{"role": "assistant", "content": "Chat cleared. What's the next mission?"}]
    st.rerun()

# 5. DISPLAY CHAT
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 6. THE PROMPT BOX
if prompt := st.chat_input("Input technical query bruv..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    with chat_placeholder:
        with st.chat_message("assistant"):
            if model and model_name != "Error":
                try:
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    if "429" in str(e):
                        st.error("🚦 Quota Full! Wait 60s.")
                    else:
                        st.error(f"Bruv, API caught an L: {e}")
            else:
                st.error("Fatal: Model offline. Check Secrets.")
