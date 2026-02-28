import streamlit as st
import os
from rag_engine import (
    build_index_from_file,
    load_existing_index,
    get_query_engine
)

st.set_page_config(page_title="Private Consultant")
st.title("🛡️ Your Private AI Consultant")

# Session memory
if "messages" not in st.session_state:
    st.session_state.messages = []

if "index" not in st.session_state:
    st.session_state.index = load_existing_index()

# Sidebar upload
uploaded_file = st.sidebar.file_uploader(
    "Upload a Business PDF",
    type="pdf"
)

if uploaded_file:
    os.makedirs("temp_files", exist_ok=True)

    file_path = os.path.join("temp_files", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.success("File uploaded successfully!")

    st.session_state.index = build_index_from_file(file_path)

    st.sidebar.success("Index built and saved successfully!")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about your document..."):

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.index is None:
        response = "Please upload a PDF first."
    else:
        query_engine = get_query_engine(st.session_state.index)
        response = query_engine.chat(prompt)
    with st.chat_message("assistant"):
        st.markdown(str(response))

    st.session_state.messages.append(
        {"role": "assistant", "content": str(response)}
    )