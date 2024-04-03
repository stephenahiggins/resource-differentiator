import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import textstat
from apikey import apikey

# Config
os.environ['OPENAI_API_KEY'] = apikey
placeholder = open("src/storage/human_rights.txt", "r").read()
llm = OpenAI(temperature=0.9)
MAX_ATTEMPTS = 3

def calculate_reading_age(text):
    fk_grade = textstat.flesch_kincaid_grade(text)
    # Convert the Flesch-Kincaid grade to a reading age. Note: This is a rough estimate.
    reading_age = round(fk_grade) + 5
    return reading_age

def correct_british_english(document, llm):
    correction_template = PromptTemplate(
        input_variables=['document'],
        template="Please correct the following text to ensure it adheres to British English standards for spelling, punctuation, grammar, and is legible. Provide only the corrected text, with no annotations or explanations: {document}"
    )
    correction_chain = LLMChain(llm=llm, prompt=correction_template, verbose=True, output_key='corrected_text')
    corrected_text_run = correction_chain.run(document=document)
    return corrected_text_run

def differentiate_and_correct_document(document, target_age, llm):
    closest_age_diff = float('inf')  # Initialize with a high difference
    closest_text = ""
    closest_attempt = 0  # Track the attempt number of the closest match

    for attempt in range(1, MAX_ATTEMPTS + 1):
        differentiation_template = PromptTemplate(
            input_variables=['target_age', 'document'],
            template="Adapt this document to suit a strict reading age of {target_age}. Where possible, keep the key points. Document: {document}"
        )
        differentiation_chain = LLMChain(llm=llm, prompt=differentiation_template, verbose=True, output_key='reading_age')
        
        with st.spinner(f'Processing for age {target_age}, attempt {attempt}...'):
            differentiation_run = differentiation_chain.run(target_age=target_age, document=document)
            current_text = differentiation_run  # Assume differentiation_run returns the text
            
            current_reading_age = calculate_reading_age(current_text)
            age_diff = abs(current_reading_age - target_age)
            if age_diff < closest_age_diff:
                closest_age_diff = age_diff
                closest_text = current_text
                closest_attempt = attempt

            # Update the warning with the latest attempt's reading age
            st.warning(f'Attempt {attempt}: Recorded reading age: {current_reading_age}')
                
    # Warn about which attempt was closest to the target age
    st.info(f'The closest match to the target age was from attempt #{closest_attempt}.')
    
    # Correct the closest matching text for British English
    corrected_text = correct_british_english(closest_text, llm)
    return corrected_text

def main():
    st.title("Learning Material Differentiation")
    st.markdown("""# Test Differentiator By Reading Age Test
* This demo takes some sample text (by default a section from the [Hodder OCR Geography A Level textbook on human rights](https://www.hoddereducation.com/media/resources/he/Geography/A-level/9781471858703/OCR-A-level-Geography-sample-chapter.pdf).
* It then uses Chat GPT to attempt to differentiate the work for the selected reading ages. 
* The content returned from ChatGPT is then checked against the Flesch Kincaid_grade.
    * This is then roughly converted to a "reading age"
* If the returned text doesn't match the absolute value of the target reading age, the request is re-run. 
    * This happens 3 times
    * If no exact match is found, then the best of 3 is taken
* Finally, the "best of 3" result is sent to Chat GPT to check for British English spelling, punctuation and grammar. """)
    content = st.text_area("Enter your content", value=placeholder, height=400)
    
    selected_ages = st.multiselect("Select target reading ages:", range(6, 20))

    if st.button('Differentiate 🚀'):
        if content:
            for age in selected_ages:
                differentiated_text = differentiate_and_correct_document(content, age, llm)
                st.header(f"Differentiated for Age {age}")
                st.write(differentiated_text)
        else:
            st.error("Please enter some content to differentiate.")

if __name__ == "__main__":
    main()
