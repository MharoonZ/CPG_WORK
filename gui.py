# app.py
import streamlit as st
from datetime import datetime
from backend_connector import get_guidelines, process_user_input

st.set_page_config(page_title="Heart Failure Guidelines Assistant", layout="centered")

st.title("Heart Failure Guidelines Assistant")
st.caption("Evidence-based recommendations powered by 2022 AHA/ACC/HFSA Guidelines chapter: 7")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.guidelines = get_guidelines()  # Load guidelines once

# Sidebar with new chat button and info
with st.sidebar:
    st.header("About")
    st.info("This assistant provides evidence-based recommendations for heart failure management based on the 2022 AHA/ACC/HFSA guidelines.")

    if st.button("🔄 New Chat"):
        st.session_state.messages = []
        st.rerun()

# Chat display using st.chat_message()
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "time" in msg:
            st.caption(f"🕒 {msg['time']}")

# Input box at bottom using chat input
if prompt := st.chat_input("Ask a question about heart failure management..."):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
        st.caption(f"🕒 {now}")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": now})

    # Prepare conversation history for LLM context
    conversation_history = [
        {"role": msg["role"], "content": msg["content"]}
        for msg in st.session_state.messages
        if msg["role"] in ["user", "assistant"]
    ]

    # Process with backend
    try:
        response = process_user_input(prompt, conversation_history)

        if response["success"]:
            recommendations = response["recommendations"]

            # Display assistant message with recommendations
            with st.chat_message("assistant"):
                st.markdown(recommendations)
                st.caption(f"🕒 {now}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": recommendations,
                "time": now
            })
        else:
            error_msg = f"Sorry, an error occurred: {response['error']}"
            with st.chat_message("assistant"):
                st.error(error_msg)
                st.caption(f"🕒 {now}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "time": now
            })

    except Exception as e:
        error_msg = f"Sorry, an error occurred: {str(e)}"
        with st.chat_message("assistant"):
            st.error(error_msg)
            st.caption(f"🕒 {now}")
        st.session_state.messages.append({
            "role": "assistant",
            "content": error_msg,
            "time": now
        })