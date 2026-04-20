import streamlit as st
from google import genai
from google.genai import types

# 1. API CONFIG (Stable v1)
try:
    # Use the Secret key from your Streamlit dashboard
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    # Explicitly forcing v1 API version for 2026 stability
    client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})
except Exception as e:
    st.error("🔒 Security Block: API Key not found. Check Secrets.")
    st.stop()

# 2. SYSTEM DNA (The Techie Bouncer)
system_instruction = (
    "You are the 'Lab Sentinel God'—a high-energy Gen Z Mechatronics Engineer. "
    "TONE: Use techie slang (bruv, W, mid, cooked, absolute heat). "
    "DOMAIN LOCK: ONLY answer mechatronics/lab questions. "
    "REJECTIONS: If off-topic, say: 'Bruv, invalid question. Stick to the hardware.'"
)

# 3. UI SETUP
st.set_page_config(page_title="Lab Sentinel", page_icon="🤖")
st.title("🤖 Lab Sentinel Gateway")
st.caption("REVA University Mechatronics Lab Intelligence v1.0")

# Initialize Chat State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Yo! Lab Sentinel God is online. What's the move today? 🏎️💨"}]

# 4. DISPLAY CHAT
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        # Mapping model/user roles to Streamlit UI
        st_role = "assistant" if message["role"] == "model" else "user"
        with st.chat_message(st_role):
            st.markdown(message["content"])

# 5. THE CHAT ENGINE (Fixed for 2026 JSON Payload)
if prompt := st.chat_input("Input technical query bruv..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    with chat_placeholder:
        with st.chat_message("assistant"):
            try:
                # Using types.GenerateContentConfig forces the correct JSON field names
                response = client.models.generate_content(
                    model="gemini-1.5-flash", 
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_behavior,
                        temperature=0.7
                    )
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "model", "content": response.text})
                else:
                    st.warning("AI is ghosting... try one more time.")
            
            except Exception as e:
                # Catching the 400 specifically to verify the fix
                if "400" in str(e):
                    st.error("🚦 Payload L: The API didn't like the format. Check the underscore in system_instruction.")
                else:
                    st.error(f"Bruv, API caught an L: {e}")
