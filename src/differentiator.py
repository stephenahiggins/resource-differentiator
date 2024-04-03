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
llm = OpenAI(temperature=0.9, max_tokens=1000)
MAX_ATTEMPTS = 3
DEBUG_DISABLE_BRITISH_ENGLISH_CORRECTION = True

READING_AGE_TO_FLESCH_KINCAID_GRADE = {
    '4': [1],
    '5': [1],
    '6': [1],
    '7': [1],
    '8': [2],
    '9': [3],
    '10': [4],
    '11': [5],
    '12': [5],
    '13': [6],
    '14': [7],
    '15': [8],
    '16': [9],
    '17': [10],
    '18': [11,12,13,14,15,16,17,18],
    '19': [11,12,13,14,15,16,17,18]
}

def reading_age_to_fk_grade(reading_age):
    try:
        return READING_AGE_TO_FLESCH_KINCAID_GRADE[str(reading_age)]
    except KeyError:
        raise ValueError(f"Reading age {reading_age} not found in dictionary.")

def fk_grade_to_reading_age(fk_grade):
    corresponding_age = False
    for age, grades in READING_AGE_TO_FLESCH_KINCAID_GRADE.items():
        if fk_grade in grades:
           corresponding_age = age
           break
    
    if corresponding_age == False:
        raise ValueError(f"Flesch-Kincaid grade {fk_grade} not found in dictionary.")
    
    return int(corresponding_age)

def calculate_fk_grade_of_text(text):
    fk_grade = textstat.flesch_kincaid_grade(text)
    fk_grade_round = round(fk_grade)
    return fk_grade_round

def calculate_reading_age_of_text(text):
    fk_grade = calculate_fk_grade_of_text(text)
    return fk_grade_to_reading_age(fk_grade)

def correct_british_english(document, llm):
    correction_template = PromptTemplate(
        input_variables=['document'],
        template="Please correct the following text to ensure it adheres to British English standards for spelling, punctuation, grammar, and is legible. Provide only the corrected text, with no annotations or explanations: {document}"
    )
    correction_chain = LLMChain(llm=llm, prompt=correction_template, verbose=True, output_key='corrected_text')
    corrected_text_run = correction_chain.run(document=document)
    return corrected_text_run

def differentiate_and_correct_document(document, target_reading_age, llm):
    fk_values_from_age = READING_AGE_TO_FLESCH_KINCAID_GRADE.get(target_reading_age)
    target_fk_grade = fk_values_from_age[0] # Assume the lowest reading age is the least risky (if more than one age is provided)
    print(f"Target FK grade: {target_fk_grade}")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        differentiation_template = PromptTemplate(
            input_variables=['target_fk_grade', 'document'],
            template="Adapt and shorten this text to match a Flesch-Kincaid Grade level of {target_fk_grade}. Only output the text, no comments or explanations. Text: {document}"
        )
        differentiation_chain = LLMChain(llm=llm, prompt=differentiation_template, verbose=False, output_key='target_reading_age')
        
        with st.spinner(f'Processing for age(s) {target_reading_age}, attempt {attempt}...'):
            differentiation_run = differentiation_chain.run(target_fk_grade=str(target_fk_grade), document=document)
            current_text = differentiation_run  # Assume differentiation_run returns the text
            # Setup "closest match" variables
            calculated_reading_age = calculate_reading_age_of_text(current_text)
            closest_age_diff = float('inf')  # Initialize with a high difference
            closest_text = ""
            closest_attempt = 0  # Track the attempt number of the closest match
            
            age_diff = abs(calculated_reading_age - int(target_reading_age))
            
            if age_diff == 0:
                # If the age difference is 0, we have an exact match
                st.success(f'Exact match found for target age {target_reading_age} in attempt {attempt}.')
                closest_text = current_text
                break
            if age_diff < closest_age_diff:
                closest_age_diff = age_diff
                closest_text = current_text
                closest_attempt = attempt
            

            # Update the warning with the latest attempt's reading age
            st.warning(f'Attempt {attempt}: Recorded reading age: {calculated_reading_age}')
                
    # Warn about which attempt was closest to the target age
    st.info(f'The closest match to the target age was from attempt #{closest_attempt}.')
    
    # Correct the closest matching text for British English
    if DEBUG_DISABLE_BRITISH_ENGLISH_CORRECTION:
        corrected_text = closest_text
    else: 
        corrected_text = correct_british_english(closest_text, llm)
    return corrected_text

def main():
    st.title("Learning Material Differentiation")
    st.markdown("""# Test Differentiator By Reading Age Test
* This demo takes some sample text (by default a section from the [Hodder OCR Geography A Level textbook on human rights](https://www.hoddereducation.com/media/resources/he/Geography/A-level/9781471858703/OCR-A-level-Geography-sample-chapter.pdf).
* It then uses Chat GPT to attempt to differentiate the work for the selected reading ages. 
* The content returned from ChatGPT is then checked against the Flesch Kincaid grade.
    * This is then roughly converted to a "reading age"
* If the returned text doesn't match the absolute value of the target reading age, the request is re-run. 
    * This happens 3 times
    * If no exact match is found, then the best of 3 is taken
* Finally, the "best of 3" result is sent to Chat GPT to check for British English spelling, punctuation and grammar. """)
    content = st.text_area("Enter your content", value=placeholder, height=400)
    selected_ages = st.multiselect("Select target reading ages:", READING_AGE_TO_FLESCH_KINCAID_GRADE.keys(), default=['6'])

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
