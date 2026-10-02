import streamlit as st
import os
from gtts import gTTS
import base64

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AuraMind AI - Pro Commercial",
    page_icon="🤖",
    layout="centered"
)

# --- INITIALIZE AGENT ---
try:
    from Agent import CommercialMasterAIAgent
    if "agent" not in st.session_state:
        st.session_state.agent = CommercialMasterAIAgent()
except ImportError:
    st.error("⚠️ Error: Could not import CommercialMasterAIAgent from Agent.py")

# --- CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR UI ---
with st.sidebar:
    st.markdown("### ⚙️ App Settings & Language")
    ui_language = st.selectbox(
        "Choose AI Response Language",
        ["Auto-Detect", "English", "Urdu", "Hindi", "Arabic", "Spanish", "French"]
    )
    
    st.markdown("---")
    st.markdown("### 🔑 Account & International")
    st.text("Phone")
    st.radio("Mode", ["Login", "Create Account"])

# --- MAIN APP HEADER ---
st.markdown("### 🤖 AuraMind AI Hub")

# --- DISPLAY CHAT HISTORY ---
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # Display clean audio player for assistant messages if available
        if message["role"] == "assistant":
            audio_file = f"temp_audio_{i}.mp3"
            if os.path.exists(audio_file):
                try:
                    with open(audio_file, "rb") as f:
                        data = f.read()
                    b64 = base64.b64encode(data).decode()
                    audio_html = f"""
                        <audio controls autoplay style="height: 35px; width: 220px; border-radius: 20px;">
                            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                        </audio>
                    """
                    st.markdown(audio_html, unsafe_allow_html=True)
                except Exception:
                    pass

# --- USER INPUT SECTION ---
user_input = st.chat_input("Ask anything (coding, business, routes, crypto)...")

if user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if "agent" in st.session_state:
                response = st.session_state.agent.process_input(user_input, selected_language=ui_language)
            else:
                response = "⚠️ Error: Agent not initialized."
            
            st.markdown(response)
            
            # Generate and save clean audio
            try:
                audio_file = f"temp_audio_{len(st.session_state.messages)}.mp3"
                tts = gTTS(text=response[:400], lang='en', slow=False)
                tts.save(audio_file)
                
                with open(audio_file, "rb") as f:
                    data = f.read()
                b64 = base64.b64encode(data).decode()
                
                audio_html = f"""
                    <audio controls autoplay style="height: 35px; width: 220px; border-radius: 20px;">
                        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                    </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
            except Exception:
                pass
                
        # Save assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()