import streamlit as st
from chatbot import chat_parallel

# Page setup
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 LangChain Chatbot")
st.write("Ask a programming, math, English, or general question.")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Run the chain
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = chat_parallel.invoke({"question": user_input})

            answer_data = result["answer"]      # ResponseSchema object
            summary_data = result["summary"]    # ResponseSchema object

            # Main answer
            st.write(answer_data.answer)

            # Structured details
            st.markdown(f"**Category:** {answer_data.category}")
            st.markdown(f"**Confidence:** {answer_data.confidence}/10")
            st.markdown(f"**Keywords:** {', '.join(answer_data.keywords)}")

            with st.expander("View Summary"):
                st.write(summary_data.summary)

    # Save assistant response to history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer_data.answer
    })

# Clear chat button
st.divider()
if st.button("🗑️ Clear Chat"):
    st.session_state.messages = []
    st.rerun()

