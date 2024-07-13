import streamlit as st
from openai import OpenAI

# Function to get the Excel formula from Groq LLM
def get_excel_formula(prompt):
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key= YOUR_GROQ_API_KEY
    )
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You're ExcelBot developed by Ansh Gupta. You can provide formula for any excel query given by user. Remember you only need to return excel formula without any extra documentation or explanation.\n"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    result = ""
    for chunk in completion:
        result += chunk.choices[0].delta.content or ""

    return result

st.title("ExcelBot")

# Text box for user input
prompt = st.text_input("Enter your Excel query:")


# Submit button
if st.button("Generate Formula"):
    if prompt:
        formula = get_excel_formula(prompt)
        st.text_area("Generated Excel Formula:", value=formula, height=200)
    else:
        st.error("Please enter a query.")
