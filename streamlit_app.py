import streamlit as st
from google import genai

# 1. CLOUD CONFIG (Zero-Leak Logic)
try:
    # Pulling from the Secret vault we set up
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("🔒 Security Block: API Key not found. Please setup Streamlit Secrets.")
    st.stop()

# 2. SYSTEM DNA (The Techie Bouncer)
system_behavior = (
    "You are the 'Lab Sentinel God'—a high-energy Gen Z Mechatronics Engineer. "
    "TONE: Use techie slang (bruv, W, mid, cooked, absolute heat) but stay elite and professional. "
    "GREETINGS: If a user says 'hi', 'hello', 'whatup', or 'yo', greet them back with techie vibes. "
    "DOMAIN LOCK: You ONLY answer questions about 3D printing, CNC, electronics (ESP32/Arduino), and lab safety. "
    "REJECTIONS: If they ask non-domain questions (flirting, life advice, 'what up baby'), "
    "say: 'Bruv, that's an invalid question. Stick to the hardware.' "
    "SUMMARIZATION: If the user asks to summarize, provide a high-speed, bulleted technical brief."
)

# 3. UI SETUP
st.set_page_config(page_title="Lab Sentinel", page_icon="🤖", layout="centered")
st.markdown("<style>.stApp { background-color: #0e1117; color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🤖 Lab Sentinel Gateway")
st.caption("REVA University Mechatronics Lab Intelligence v1.0")

# Initialize Chat State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Yo! Lab Sentinel God is online. What's the move today? 🏎️💨"}]

# Sidebar
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = [{"role": "model", "content": "History cleared. New mission starting."}]
    st.rerun()

# 4. DISPLAY CHAT
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        # Mapping roles for Streamlit UI
        st_role = "assistant" if message["role"] == "model" else "user"
        with st.chat_message(st_role):
            st.markdown(message["content"])

# 5. THE CHAT ENGINE
if prompt := st.chat_input("Input technical query bruv..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    # Generate Response
    with chat_placeholder:
        with st.chat_message("assistant"):
            try:
                # Using 1.5-Flash-8B for max speed and high quota limits
                response = client.models.generate_content(
                    model="gemini-1.5-flash-8b", 
                    contents=prompt,
                    config={'system_instruction': system_behavior}
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "model", "content": response.text})
                else:
                    st.error("Empty response from AI. Try again.")
            
            except Exception as e:
                if "429" in str(e):
                    st.error("🚦 Quota Full! Google is gatekeeping. Wait 60s.")
                else:
                    st.error(f"Bruv, API caught an L: {e}")
