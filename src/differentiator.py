import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
import textstat

# Replace with your OpenAI API key
from apikey import apikey
os.environ['OPENAI_API_KEY'] = apikey

MAX_ATTEMPTS = 3

llm = OpenAI(temperature=0.9)

def calculate_reading_age(text):
    return textstat.flesch_kincaid_grade(text)

def differentiate_document(document, target_age):
    attempts = 0
    matched_age = False  # To track if a match was found
    MAX_ATTEMPTS = 3  # Avoid infinite loops, adjust as needed
    while attempts < MAX_ATTEMPTS and not matched_age:
        attempts += 1
        # Template
        differentiation_template = PromptTemplate(
            input_variables=['target_age', 'document'],
            template="Adapt this document to suit a reading age of {target_age}. Document: {document}"
        )
        differentiation_chain = LLMChain(llm=llm, prompt=differentiation_template, verbose=True, output_key='reading_age')
        
        # Use spinner to show loading message
        with st.spinner(f'Processing for age {target_age}, attempt {attempts}...'):
            differentiation_run = differentiation_chain.run(target_age=target_age, document=document)
            output_text = differentiation_run  # Assuming differentiation_run returns the text directly

            current_reading_age = calculate_reading_age(output_text)
            if abs(current_reading_age - target_age) <= 1:  # Considering a close match as successful
                matched_age = True
                return output_text  # If reading age matches target, return the result
            else:
                st.warning(f'Recorded reading age: {current_reading_age}')
                document = output_text  # Use the output as the new input for the next attempt
        
    if not matched_age:
        st.warning("Generated text doesn't perfectly match the target reading age. Showing the closest match.")
    
    return output_text

def main():
    st.title("Learning Material Differentiation")
    placeholder = """Case study: The Transition Town movement Transition Network was founded in 2007 as a response to the twin threats of climate change and peak oil (the point in time when the maximum rate of extraction of oil is reached, after which the rate of production is expected to enter terminal decline). Since then it can be said to have gone on to tackle many other issues including some associated with globalisation such as dilution of place identity and loss of community and economy. One of the founders, Rob Hopkins, says ‘It’s about what you can create with the help of the people who live in your street, reimagining and rebuilding your neighbourhood, your town. If enough people do it, it can lead to real impact, to real jobs and real transformation of the places we live, and beyond.’ There are now over 1,200 Transition initiatives worldwide and increasing numbers of places are embracing a life where communities come together to share skills, grow food, provide care for dependents and fight inequality."""
    content = st.text_area("Enter your content", value=placeholder, height=400)
    
    selected_ages = st.multiselect(
        "Select target reading ages:", range(6, 20)
    )

    if st.button('Differentiate 🚀'):
        if content:
            # Process document for each selected age
            for age in selected_ages:
                differentiated_text = differentiate_document(content, age)
                st.header(f"Differentiated for Age {age}")
                st.write(differentiated_text)
        else:
            st.error("Please enter some content to differentiate.")

if __name__ == "__main__":
    main()
