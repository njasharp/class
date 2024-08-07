import ollama
import streamlit as st
import httpx

st.set_page_config(layout="wide")
st.title("InsightBot LLM Chatbot")
st.text("Analyzing data for making business-critical decisions and effectively handling complex analysis")

# Initialize history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Initialize models and system prompt
if "model" not in st.session_state:
    st.session_state["model"] = ""
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = ""
if "new_message" not in st.session_state:
    st.session_state["new_message"] = False

st.sidebar.write("Query Assist AI")
# Sidebar menu
with st.sidebar:
    try:
        models = [model["name"] for model in ollama.list()["models"]]
        st.session_state["model"] = st.selectbox("Choose your model", models)
    except httpx.ConnectError:
        st.error("Unable to connect.")
    st.session_state["system_prompt"] = st.text_area("System Prompt")
    
    if st.button("Reset"):
        st.session_state["messages"] = []
        st.session_state["new_message"] = False
        st.rerun()

def model_res_generator():
    messages = st.session_state["messages"]
    if st.session_state["system_prompt"]:
        messages = [{"role": "system", "content": st.session_state["system_prompt"]}] + messages
    try:
        stream = ollama.chat(
            model=st.session_state["model"],
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            yield chunk["message"]["content"]
    except httpx.ConnectError:
        st.error("Unable to connect to the local Ollama instance. Please ensure it is running.")
        return

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Add some space before the query box
st.write("")
st.write("")

if st.session_state["new_message"]:
    st.session_state["user_query"] = ""
    st.session_state["new_message"] = False
    st.rerun()

if prompt := st.text_input("What is your query?", key="user_query"):
    # Add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            message = "".join(model_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message})

    # Set flag for new message
    st.session_state["new_message"] = True
    st.rerun()

st.sidebar.info("built by dw")
