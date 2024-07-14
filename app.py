import streamlit as st
from openai import OpenAI

class ExcelBot:
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )

    # Method to get the formula from Groq LLM based on the selected platform
    def get_formula(self, prompt: str, platform: str) -> str:
        system_content = (
            "You're a Bot developed by Ansh Gupta. You can provide formulas for any query given by the user. "
            "Remember you only need to return the formula without any extra documentation or explanation.\n"
            f"Platform: {platform}"
        )
        completion = self.client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=True,
            stop=None,
        )

        result: str = ""

        for chunk in completion:
            result += chunk.choices[0].delta.content or ""

        return result

st.title("ExcelBot")
bot_instance = ExcelBot("YOUR_API_KEY")

# Text box for user input
prompt = st.text_input("Enter your query: ")

# Radio button for platform selection
platform = st.radio("Select the platform: ", ["Excel", "Google Sheets", "Airtable"])

# Submit button
if st.button("Generate Formula"):
    if prompt:
        formula = bot_instance.get_formula(prompt, platform)
        if formula:
            st.text_area("Generated Formula:", value=formula, height=100)
        else:
            st.text_area("Unable to generate formula.", height=100)
    else:
        st.error("Please enter a query.")
