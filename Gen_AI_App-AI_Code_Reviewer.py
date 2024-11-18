import streamlit as st
import google.generativeai as genai
import re

st.title("An AI Python Code Reviewer")
user_code = st.text_area("Enter your Python code here...")


f = open(r"G:\Innomatics-Data Science\GenAI\Key\Geminikey.txt","r")
key = f.read()

genai.configure(api_key = key)

instruction_to_system = """Analyze the code snippet given by user and generate type of errors in the code 
                        and generate the correct code snippet to the user."""


def generating_response(user_code):
    model = genai.GenerativeModel(model_name  = "gemini-1.5-flash",system_instruction=instruction_to_system)
    user_prompt = user_code
    response  = model.generate_content(user_prompt)
    return response.text

def fixed_code(response_string):
    match = re.search("```python(.*?)```", response_string, re.DOTALL)
    if match:
        return match.group(1).strip()

def bug_report(response_string):
    l = []
    pattern = r"^\d+\..*"
    matches = re.findall(pattern, response_string, re.MULTILINE)
    for match in matches:
        l.append(match)
    return l

if st.button("Generate"):
    generated_response = generating_response(user_code)
    st.header("Code Review")
    st.subheader("Bug Report")
    bug_report_list = bug_report(generated_response)
    st.write("The identified bugs in the user code are as follows:")
    for i in bug_report_list:
        st.write(i)
    st.subheader("Fixed Code")
    code = fixed_code(generated_response)
    st.code(code, language="python")
    