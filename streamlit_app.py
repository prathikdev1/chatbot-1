import streamlit as st
from google import genai

# 1. API CONFIG (Zero-Leak)
try:
    # Pulling from Streamlit Secrets - ensures your key stays private
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error("🔒 Security Block: API Key not found. Check Streamlit Secrets.")
    st.stop()

# 2. SYSTEM DNA (The Techie Bouncer)
system_behavior = (
    "You are the 'Lab Sentinel God'—a high-energy Gen Z Mechatronics Engineer. "
    "TONE: Use techie slang (bruv, W, mid, cooked, absolute heat) but stay elite and professional. "
    "GREETINGS: If a user says 'hi', 'hello', 'whatup', or 'yo', greet them back with techie vibes. "
    "DOMAIN LOCK: You ONLY answer technical questions about 3D printing, CNC, electronics (ESP32/Arduino), and lab safety. "
    "REJECTIONS: If they ask non-domain questions (rizz, life advice, 'what up baby'), "
    "say: 'Bruv, that's an invalid question. Stick to the hardware.' "
    "SUMMARIZATION: If requested, provide a high-speed, bulleted technical brief."
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
st.sidebar.success("Model: Gemini 3.1 Flash Lite")
st.sidebar.info("Quota: 500 Requests/Day")
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.messages = [{"role": "model", "content": "History cleared. New mission starting."}]
    st.rerun()

# 4. DISPLAY CHAT
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        # Mapping roles for Streamlit UI (user/assistant)
        st_role = "assistant" if message["role"] == "model" else "user"
        with st.chat_message(st_role):
            st.markdown(message["content"])

# 5. THE CHAT ENGINE (The Loop of Life)
if prompt := st.chat_input("Input technical query bruv..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    with chat_placeholder:
        with st.chat_message("assistant"):
            # We try the high-quota 3.1 first, then the stable 2.0/1.5
            potential_models = ["gemini-3.1-flash", "gemini-1.5-flash"]
            response_received = False
            
            for m_name in potential_models:
                try:
                    response = client.models.generate_content(
                        model=m_name, 
                        contents=prompt,
                        config={'system_instruction': system_behavior}
                    )
                    if response.text:
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "model", "content": response.text})
                        response_received = True
                        break # Exit the loop once we get a W
                except Exception as e:
                    if "404" in str(e):
                        continue # Try the next model in the list
                    else:
                        st.error(f"Bruv, API caught an L: {e}")
                        break
            
            if not response_received:
                st.error("🚦 Total Blackout: No models found. Check API Version.")
