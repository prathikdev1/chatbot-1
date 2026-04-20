import streamlit as st
from google import genai

# 1. API CONFIG (The Beta Path to Peace)
try:
    API_KEY = st.secrets["GEMINI_KEY"].strip()
    # Switching back to v1beta to find the 3.1 model
    client = genai.Client(api_key=API_KEY, http_options={'api_version': 'v1beta'})
except Exception as e:
    st.error("🔒 Security Block: API Key not found. Check Secrets.")
    st.stop()

# 2. SYSTEM DNA
sentinel_dna = (
    "SYSTEM INSTRUCTION: You are the 'Lab Sentinel God', a high-energy Gen Z Mechatronics Engineer. "
    "Use techie slang (bruv, W, mid, cooked, absolute heat). Only answer technical lab questions. "
    "If off-topic, say: 'Bruv, invalid question. Stick to the hardware.' "
    "USER QUERY: "
)

# 3. UI SETUP
st.set_page_config(page_title="Lab Sentinel", page_icon="🤖")
st.title("🤖 Lab Sentinel Gateway")
st.caption("REVA University Mechatronics Lab Intelligence v1.0")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "model", "content": "Yo! Lab Sentinel God is online. Inner peace achieved. 🏎️💨"}]

# 4. DISPLAY CHAT
chat_placeholder = st.container()
with chat_placeholder:
    for message in st.session_state.messages:
        st_role = "assistant" if message["role"] == "model" else "user"
        with st.chat_message(st_role):
            st.markdown(message["content"])

# 5. THE CHAT ENGINE (The 500-Quota Goat)
if prompt := st.chat_input("Input technical query bruv..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    with chat_placeholder:
        with st.chat_message("assistant"):
            try:
                # Targeted model on the v1beta route
                response = client.models.generate_content(
                    model="gemini-3.1-flash-lite-preview", 
                    contents=f"{sentinel_dna}{prompt}"
                )
                
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "model", "content": response.text})
                else:
                    st.warning("AI is mediatating... try again.")
            
            except Exception as e:
                # If 404 happens here, we fallback to the only other possible name
                if "404" in str(e):
                    try:
                        response = client.models.generate_content(
                            model="gemini-1.5-flash", 
                            contents=f"{sentinel_dna}{prompt}"
                        )
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "model", "content": response.text})
                    except Exception as e2:
                        st.error(f"Bruv, even the fallback is cooked: {e2}")
                else:
                    st.error(f"Bruv, API caught an L: {e}")
