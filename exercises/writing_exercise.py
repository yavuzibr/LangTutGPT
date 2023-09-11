from apikey import api_key
from langchain.chat_models import ChatOpenAI
import streamlit as st
from langchain.prompts.chat import SystemMessage, HumanMessage

# App Framework
st.set_page_config(page_title="LangTutGPT", page_icon="🤖")
st.title("Writing Exercise")
topic = st.text_input("Choose a topic: ")
character_limit = st.number_input("Choose maximum character size", value=100, step=50)
text = st.text_area("Enter your text here ", max_chars=character_limit)
start_button = st.button("Start")

# LLM
chat = ChatOpenAI(
    openai_api_key=api_key,
    temperature=0,
    model='gpt-3.5-turbo'
)
messages = [SystemMessage(
    content=("You are a language exam judge.You will examine the text given to you by the user,whether the variety "
             "and based on grammatical rules, the variety of words in the text, and whether the content of the text "
             f"matches the {topic},give a score out of 10 and give feedback on areas that need improvement.")),
    HumanMessage(content=f"{text}")

]

response = chat(messages)
if start_button:
    st.write("Your text:")
    st.write(text)
    st.write("My review: ")
    st.write(response.content)
