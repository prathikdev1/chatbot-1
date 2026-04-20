import streamlit as st
from google import genai
from google.genai import types

# 1. API CONFIG
try:
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    # Explicitly setting the client for 2026 stability
    client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1'})
except Exception as e:
    st.error("🔒 Security Block: API Key not found. Check Secrets.")
    st.stop()

# 2. SYSTEM DNA
system_behavior = (
    "You are the 'Lab Sentinel God'—a high-energy Gen Z Mechatronics Engineer. "
    "TONE: Gen Z slang (bruv, W, mid, cooked, heat). "
    "DOMAIN: Mechatronics lab stuff only."
)

# 3. UI SETUP
st.set_page_config(page_title="Lab Sentinel", page_icon="🤖")
st.title("🤖 Lab Sentinel Gateway")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. THE CHAT ENGINE (Simplified for Debugging)
if prompt := st.chat_input("Input technical query bruv..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # We are using the most generic ID possible to force a connection
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_behavior
                )
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "model", "content": response.text})
        
        except Exception as e:
            st.error(f"Bruv, the API is still cooked: {e}")
            # This will print the FULL error in the logs so we can see the real L
            print(f"DEBUG ERROR: {e}")
