import ollama
import streamlit as st

st.set_page_config(layout="wide")
st.title("LLM Chatbot")

# Initialize history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Initialize models and system prompt
if "model" not in st.session_state:
    st.session_state["model"] = ""
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = ""
if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""

# Sidebar menu
with st.sidebar:
    models = [model["name"] for model in ollama.list()["models"]]
    st.session_state["model"] = st.selectbox("Choose your model", models)
    st.session_state["system_prompt"] = st.text_area("System Prompt")
    
    if st.button("Reset"):
        st.session_state["messages"] = []
        st.session_state["user_query"] = ""
        st.rerun()

def model_res_generator():
    messages = st.session_state["messages"]
    if st.session_state["system_prompt"]:
        messages = [{"role": "system", "content": st.session_state["system_prompt"]}] + messages
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Add some space before the query box
st.write("")
st.write("")

if prompt := st.text_input("What is your query?", key="user_query"):
    # Add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            message = "".join(model_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message})

    # Clear the input box for new query
    st.session_state["user_query"] = ""
    st.rerun()

st.sidebar.info("built by dw")
In this version:

Initialized st.session_state["user_query"] if it's not already set.
Managed the query box state by resetting st.session_state["user_query"] before calling st.rerun().
this code loops on same answer be sure to stop after answer and clear query for next answer -import ollama
import streamlit as st

st.set_page_config(layout="wide")
st.title("LLM Chatbot")

# Initialize history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Initialize models and system prompt
if "model" not in st.session_state:
    st.session_state["model"] = ""
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = ""

# Sidebar menu
with st.sidebar:
    models = [model["name"] for model in ollama.list()["models"]]
    st.session_state["model"] = st.selectbox("Choose your model", models)
    st.session_state["system_prompt"] = st.text_area("System Prompt")
    
    if st.button("Reset"):
        st.session_state["messages"] = []
        st.experimental_rerun()

def model_res_generator():
    messages = st.session_state["messages"]
    if st.session_state["system_prompt"]:
        messages = [{"role": "system", "content": st.session_state["system_prompt"]}] + messages
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Add some space before the query box
st.write("")
st.write("")

if prompt := st.text_input("What is your query?", key="user_query"):
    # Add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            message = "".join(model_res_generator())
        st.session_state["messages"].append({"role": "assistant", "content": message})

    # Clear the input box for new query
    st.experimental_rerun()

st.sidebar.info("built by dw")
ChatGPT
To stop the loop and ensure the query box is cleared after an answer, you can use a flag to indicate when a new message has been added. This way, the input box will be reset only once the assistant's response is processed. Here is the corrected code:

python
Copy code
import ollama
import streamlit as st

st.set_page_config(layout="wide")
st.title("LLM Chatbot")

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

# Sidebar menu
with st.sidebar:
    models = [model["name"] for model in ollama.list()["models"]]
    st.session_state["model"] = st.selectbox("Choose your model", models)
    st.session_state["system_prompt"] = st.text_area("System Prompt")
    
    if st.button("Reset"):
        st.session_state["messages"] = []
        st.session_state["new_message"] = False
        st.experimental_rerun()

def model_res_generator():
    messages = st.session_state["messages"]
    if st.session_state["system_prompt"]:
        messages = [{"role": "system", "content": st.session_state["system_prompt"]}] + messages
    stream = ollama.chat(
        model=st.session_state["model"],
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        yield chunk["message"]["content"]

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
    st.experimental_rerun()

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
    st.experimental_rerun()

st.sidebar.info("built by dw")
In this updated code:

Added a new_message flag to track when a new message has been added.
After generating a response and adding it to the messages list, set the new_message flag to True and rerun the app.
On the next run, check the new_message flag to clear the query input and reset the flag before rerunning the app again.
what is the requirement text
ChatGPT
Here is the requirements.txt file for the Streamlit app, which includes the necessary dependencies for the provided code:

Copy code
streamlit
ollama
Make sure you have these libraries installed. If you are using a virtual environment, you can create this requirements.txt file in the same directory as your Streamlit script, and then install the dependencies by running:

sh
Copy code
pip install -r requirements.txt
This will ensure that both Streamlit and the ollama package are installed in your environment.

i am deploying on streamlit - can you add a error msg if user in not on locall ollam - httpx.ConnectError: 
ChatGPT
To handle the httpx.ConnectError and show an error message if the user is not on a local Ollama instance, you can add error handling in the model_res_generator function. Here is the updated code:

python
Copy code
import ollama
import streamlit as st
import httpx

st.set_page_config(layout="wide")
st.title("LLM Chatbot")

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

# Sidebar menu
with st.sidebar:
    try:
        models = [model["name"] for model in ollama.list()["models"]]
        st.session_state["model"] = st.selectbox("Choose your model", models)
    except httpx.ConnectError:
        st.error("Unable to connect to the local Ollama instance. Please ensure it is running.")
    st.session_state["system_prompt"] = st.text_area("System Prompt")
    
    if st.button("Reset"):
        st.session_state["messages"] = []
        st.session_state["new_message"] = False
        st.experimental_rerun()

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
    st.experimental_rerun()

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
    st.experimental_rerun()

st.sidebar.info("built by dw")
