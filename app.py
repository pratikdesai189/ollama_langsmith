import os
import dotenv

from langchain_ollama import OllamaLLM
dotenv.load_dotenv()
import streamlit as st

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


## Langsmith Tracking
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"]=os.getenv("LANGCHAIN_PROJECT")

prompt=ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant Please respond to the questions asked."),
        ("user", "Question: {question}")
    ]
)

st.title("Ollama + LangSmith")
input_text=st.text_input("Ask a question to the assistant:")
llm=OllamaLLM(model="gemma:2b")
output_parser=StrOutputParser()
chain=prompt | llm | output_parser

if input_text:
    with st.spinner("Thinking..."):
        response=chain.invoke({"question": input_text})
        st.write(response)


