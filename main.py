import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import SequentialChain, LLMChain
import os
from apikey import api_key, serp_api_key
from langchain.utilities import WikipediaAPIWrapper
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.prompts import PromptTemplate

# API Key Configuration
os.environ["OPENAI_API_KEY"] = api_key
os.environ["SERPAPI_API_KEY"] = serp_api_key

# App framework
st.set_page_config(page_title='LangTutGPT', page_icon='🤖')
st.title('🤖LangTutGPT👨🏻‍🏫')
introduction_text = "Hello Fellow Learner! I am LangTutGPT. I’ll help you with learning new languages. "
st.text(introduction_text)
languages = ['Turkish', 'English', 'French', 'German', 'Japanese', 'Korean']
levels = ['Beginner', 'Intermediate', 'Advanced']
language = st.selectbox("Choose a language:", languages)
level = st.selectbox("Choose your level:", levels)
start_button = st.button("Start")

# LLM
llm = OpenAI(temperature=0.5, model_name='gpt-3.5-turbo')

# Why should I learn / What are the benefits of learning ?
q1 = PromptTemplate(input_variables=['language'],
                    template="Explain Why is learning {language} is important and What are the benefits of it ?")



chain = LLMChain(llm=llm, prompt=q1)
wiki = WikipediaAPIWrapper()
wiki_template = PromptTemplate(input_variables=['language', 'wiki_search'],
                               template='Make a wikipedi search:{wiki_search} about the history of {language} language')
wiki2_template = PromptTemplate(input_variables=['language', 'wiki_search'],
                                template='Make a wikipedia search:{wiki_search} about the guideline used to describe '
                                         'the achievement of the learners of {language}'
                                )
# Agents
tools = load_tools(['serpapi'], llm=llm)
agent = initialize_agent(tools, llm, agent='zero-shot-react-description')

if start_button:
    st.write(f"So you want to learn {language} and your level is {level}. Cool! Let’s start with answering some "
             f"question about learning {language}")
    st.subheader(f"Why should I learn {language}?")
    response = chain.run(language)
    st.write(response)
    st.subheader(f"What history does {language} language have?")
    wikipedia = wiki.run(language)
    st.write(wikipedia)
    st.subheader(f"What are the dialects and accents of {language}?")
    agentq = agent.run(language)
    st.write(agentq)
    st.subheader(f"What are the guideline used to describe the achievement of the learners of {language}")
    wikipedia2=wiki.run(language)
    st.write(wikipedia2)
