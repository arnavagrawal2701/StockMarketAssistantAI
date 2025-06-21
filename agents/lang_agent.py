# agents/lang_agent.py

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

def generate_tickers(data_text):
    prompt_template = "Extract the correct stock ticker symbols from the following user query. \
    - If only a company name is mentioned, infer the correct Yahoo Finance-compatible ticker symbol. \
    - Use exchange-specific tickers if needed (e.g., use `.NS` for NSE India, `.BO` for BSE India, `.NY` for NYSE, etc.).\
    - Only return valid ticker symbols that can be directly used with Yahoo Finance or stock APIs.\
    - Output format: uppercase tickers, comma-separated, no spaces, no explanations.\
    User query: {transcript}"

    prompt = PromptTemplate.from_template(prompt_template)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3,
    )

    chain = prompt | llm

    response = chain.invoke({"transcript": data_text})
    return response.content

def generate_brief(data_text):
    prompt_template = "Generate a concise spoken market brief using this data:\n{transcript}"

    prompt = PromptTemplate.from_template(prompt_template)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro-latest",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3,
    )

    chain = prompt | llm

    response = chain.invoke({"transcript": data_text})
    return response.content
