from dotenv import load_dotenv
import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


# loading the env to access the openai model using api key
load_dotenv(dotenv_path=r"api_key.env")
os.environ["OPENAI_API_KEY"] = os.getenv("openai_api")

# taking text file input from user , using streamlit to do the same
st.title("📝TEXT SUMMARIZER")
st.caption('''This project includes the summarization of the large text into small summary.\nHere user will upload the text file which has large content in it.\n The AI Model will generate the summary for you.''')


upload_file = st.file_uploader("choose text file", type='txt')

if upload_file is not None:
    try:
        file_name = upload_file.name

        # creating a button to read the file
        open_file_button = st.button(
            "READ FILE DATA", use_container_width=True)

        # reading the file data
        if open_file_button:
            data = upload_file.read().decode('utf-8')
            st.session_state['data'] = data
            st.subheader("FILE DATA")
            st.markdown(data)

    except Exception as e:
        st.error("----------ERROR-----------\n", e)

    # creating prompt to the model
    prompt = PromptTemplate.from_template(
        '''you area professional text summarizer you have to make the summary in {summary_style} style.
        you have to generate summary for the text shared.
        read the text and make a short and comprehensive summary for the same
        keep the  text in bullet points if required 
        make it look presentable 
        create the summary in {max_lines} lines.
        you can make the use of professional emoji if required.
        here is the file input :{input}''')

    # loading the openai model
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)

    # output
    output = StrOutputParser()

    # creating a chain
    chain = prompt | llm | output

    st.subheader("✅SELECT LINES AND STYLES:")

    # creating slider and drop down
    max_lines = st.slider(label="MAX LINES", min_value=1, max_value=100)

    summary_style = st.selectbox(label='Summary Style', options=[
                                 'Professional', 'Simple', 'Technical', 'Student Friendly'])

    # invoking the model
    generate_button = st.button("GENERATE RESPONSE", use_container_width=True)
    if generate_button:
        try:
            if 'data' not in st.session_state:
                st.error("THERE IS NOT DATA!!")
            else:
                with st.spinner("GENERATING RESPONSE...."):
                    response = chain.invoke(
                        {"input": st.session_state['data'],
                         "max_lines": max_lines,
                         "summary_style": summary_style})
                    st.session_state['response'] = response

                    st.subheader("AI RESPONSE")
                    st.markdown(response)

        except Exception as e:
            st.error(f"{e}")

    # creating a download button to downaload the file
    if 'response' in st.session_state:
        download = st.download_button(
            label='DOWNLOAD FILE',
            data=st.session_state['response'],
            file_name="file_summary.txt",
            mime='text/plain',
            width='stretch'
        )
        if download:
            st.success("file downloaded!!!")
