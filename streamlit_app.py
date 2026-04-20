import streamlit as st
from google import genai  # The 2026 Official SDK

# 1. API CONFIG (Zero-Leak)
try:
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("🔒 Security Block: API Key not found or invalid. Check Secrets.")
    st.stop()

# 2. SYSTEM DNA
system_behavior = (
    "You are the 'Lab Sentinel God'—a high-energy Gen Z Mechatronics Engineer. "
    "TONE: Use techie slang (bruv, W, mid, cooked, absolute heat) but stay elite and professional. "
    "GREETINGS: If a user says 'hi', 'hello', 'whatup', or 'yo', greet them back with techie vibes. "
    "DOMAIN LOCK: You ONLY answer technical mechatronics lab questions. "
    "REJECTIONS: For off-topic stuff, say: 'Bruv, invalid question. Stick to the hardware.' "
    "SUMMARIZATION: Use bullet points for high-speed technical briefs."
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
    st.session_state.messages = [{"role": "model", "content": "Chat cleared. What's the next mission?"}]
    st.rerun()

# 4. DISPLAY CHAT
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        # Note: New SDK uses 'model' instead of 'assistant'
        role = "assistant" if message["role"] == "model" else "user"
        with st.chat_message(role):
            st.markdown(message["content"])

# 5. THE PROMPT BOX
if prompt := st.chat_input("Input technical query bruv..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    with chat_placeholder:
        with st.chat_message("assistant"):
            try:
                # 2026 Model Call Syntax
                response = client.models.generate_content(
                    model="gemini-2.0-flash", # Stable 2026 goat
                    contents=prompt,
                    config={'system_instruction': system_behavior}
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
            except Exception as e:
                if "429" in str(e):
                    st.error("🚦 Quota Full! Wait 60s.")
                else:
                    st.error(f"Bruv, API caught an L: {e}")
