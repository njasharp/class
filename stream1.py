import ollama
import streamlit as st
import httpx
import io
import pandas as pd
from PyPDF2 import PdfReader
from PIL import Image

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
    st.session_state["system_prompt"] = "analyze file and summarize in bullet points"
if "new_message" not in st.session_state:
    st.session_state["new_message"] = False
if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""
if "uploaded_file_content" not in st.session_state:
    st.session_state["uploaded_file_content"] = ""
if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = []

st.sidebar.write("Query Assist AI")
# Sidebar menu
with st.sidebar:
    try:
        models = [model["name"] for model in ollama.list()["models"]]
        st.session_state["model"] = st.selectbox("Choose your model", models)
    except httpx.ConnectError:
        st.error("Unable to connect.")
    st.session_state["system_prompt"] = st.text_area("System Prompt", value="analyze file and summarize in bullet points")
    
    if st.button("Reset"):
        st.session_state["messages"] = []
        st.session_state["new_message"] = False
        st.session_state["user_query"] = ""
        st.session_state["uploaded_file_content"] = ""
        st.session_state["uploaded_files"] = []
        st.rerun()

    uploaded_files = st.file_uploader("Upload images (PNG, JPG) or text files (PDF, CSV)", type=["png", "jpg", "pdf", "csv"], accept_multiple_files=True)
    if uploaded_files:
        st.session_state["uploaded_files"] = uploaded_files

    # Add a radio button to decide if the uploaded file should be part of the query
    include_files_in_query = st.radio("Include uploaded files in query?", ("Yes", "No"))

def process_uploaded_files():
    file_contents = []
    image_files = []
    for uploaded_file in st.session_state["uploaded_files"]:
        file_type = uploaded_file.type
        if "image" in file_type:
            image_files.append(uploaded_file)
            file_contents.append(f"Image file: {uploaded_file.name}")
        elif "pdf" in file_type:
            pdf_reader = PdfReader(io.BytesIO(uploaded_file.read()))
            pdf_text = ""
            for page in pdf_reader.pages:
                pdf_text += page.extract_text()
            file_contents.append(f"PDF file: {uploaded_file.name}\nContent:\n{pdf_text}")
        elif "csv" in file_type:
            csv_data = pd.read_csv(uploaded_file)
            csv_text = csv_data.to_string()
            file_contents.append(f"CSV file: {uploaded_file.name}\nContent:\n{csv_text}")
    return "\n".join(file_contents), image_files

def model_res_generator(messages):
    try:
        stream = ollama.chat(
            model=st.session_state["model"],
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            yield chunk["message"]["content"]
    except (httpx.ConnectError, ollama.ResponseError) as e:
        st.error(f"An error occurred: {e}")
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
    # Process and include uploaded file content in the query if the user chose to include it
    if include_files_in_query == "Yes":
        st.session_state["uploaded_file_content"], image_files = process_uploaded_files()
        augmented_prompt = prompt + "\n\n" + st.session_state["uploaded_file_content"]
    else:
        augmented_prompt = prompt

    # Prepare messages with possible images
    messages = [{"role": "user", "content": augmented_prompt}]
    if st.session_state["system_prompt"]:
        messages.insert(0, {"role": "system", "content": st.session_state["system_prompt"]})
    if include_files_in_query == "Yes" and image_files:
        with io.BytesIO() as file_obj:
            file_obj.write(image_files[0].read())
            file_obj.seek(0)
            messages[0]["images"] = [file_obj.read()]
    
    # Add latest message to history in format {role, content}
    st.session_state["messages"].append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Generate response based on the augmented prompt
            try:
                message = "".join(model_res_generator(messages))
                st.session_state["messages"].append({"role": "assistant", "content": message})
            except Exception as e:
                st.error(f"Failed to generate response: {e}")

    # Set flag for new message
    st.session_state["new_message"] = True
    st.rerun()

st.sidebar.info("built by dw")
