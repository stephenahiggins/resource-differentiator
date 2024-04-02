import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

# Replace with your OpenAI API key
from apikey import apikey
os.environ['OPENAI_API_KEY'] = apikey

st.set_page_config(
        page_title="Differentiator",
)

llm = OpenAI(temperature=0.9)

def differentiate_document(document, target_age):
    # Template
    differentiation_template = PromptTemplate(
        input_variables=['target_age', 'document'],
        template="Adapt this document to suit a reading age of {target_age}. Document: {document}"
    )
    differentiation_chain = LLMChain(llm=llm, prompt=differentiation_template, verbose=True, output_key='reading_age')
    differentiation_run = differentiation_chain.run(target_age=target_age, document=document)
    # Use spinner to show loading message
    with st.spinner(f'Processing for age {target_age}...'):
        differentiation_run = differentiation_chain.run(target_age=target_age, document=document)
    return differentiation_run

def main():
    st.title("Learning Material Differentiation")
    placeholder = """Case study: The Transition Town movement Transition Network was founded in 2007 as a response to the twin threats of climate change and peak oil (the point in time when the maximum rate of extraction of oil is reached, after which the rate of production is expected to enter terminal decline). Since then it can be said to have gone on to tackle many other issues including some associated with globalisation such as dilution of place identity and loss of community and economy. One of the founders, Rob Hopkins, says ‘It’s about what you can create with the help of the people who live in your street, reimagining and rebuilding your neighbourhood, your town. If enough people do it, it can lead to real impact, to real jobs and real transformation of the places we live, and beyond.’ There are now over 1,200 Transition initiatives worldwide and increasing numbers of places are embracing a life where communities come together to share skills, grow food, provide care for dependents and fight inequality."""
    content = st.text_area("Enter your content", value=placeholder, height=400)
    
    selected_ages = st.multiselect(
        "Select target reading ages:", range(6, 20)
    )

    # Added 'Go' button
    if st.button('Differentiate'):
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
