import streamlit as st

st.set_page_config(
    page_title="Gen AI API's exploration",
    page_icon="👋"
)

st.write("# Welcome to demo of Gen AI Api's exploration! 👋")

st.sidebar.success("Select a demo above.")

with open('./README.md', 'r') as file:
    readme = file.read()

st.markdown(readme)