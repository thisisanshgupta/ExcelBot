import streamlit as st
from openai import OpenAI

# Function to get the formula from Groq LLM based on the selected platform
def get_formula(prompt, platform):
    client = OpenAI(
        base_url="https://api.groq.com/openai/v1",
        api_key=ENTER_YOUR_API_KEY
    )
    system_content = (
        "You're a Bot developed by Ansh Gupta. You can provide formulas for any query given by the user. "
        "Remember you only need to return the formula without any extra documentation or explanation.\n"
        f"Platform: {platform}"
    )
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": system_content
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
prompt = st.text_input("Enter your query:")

# Radio button for platform selection
platform = st.radio("Select the platform:", ["Excel", "Google Sheets", "Airtable"])

# Submit button
if st.button("Generate Formula"):
    if prompt:
        formula = get_formula(prompt, platform)
        st.text_area("Generated Formula:", value=formula, height=100)
    else:
        st.error("Please enter a query.")
