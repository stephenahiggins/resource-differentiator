# Differentiator By Reading Age Test
## About The Project
* This demo uses some default text from the [Hodder OCR Geography A Level textbook on human rights](https://www.hoddereducation.com/media/resources/he/Geography/A-level/9781471858703/OCR-A-level-Geography-sample-chapter.pdf). This can be overwritten.
* It then uses Chat GPT to attempt to differentiate the work for the selected reading ages. 
* The content returned from ChatGPT is then checked against the Flesch Kincaid_grade.
    * This is then roughly converted to a "reading age"
* If the returned text doesn't match the absolute value of the target reading age, the request is re-run. 
    * This happens 3 times
    * If no exact match is found, then the best of 3 is taken
* Finally, by setting the `DEBUG_DISABLE_BRITISH_ENGLISH_CORRECTION` to `True`, the "best of 3" result is sent to Chat GPT to check for British English spelling, punctuation and grammar. 

##  Notes & Observations
* The results tend to be better towards the middle of the available reading ages (it's a bell curve of accuracy). 
* I'm not sure that Flesch-Kincaid is the best way of _checking the marking_. There's possibly other ways to do it.
* There's still the chance of hallucinations. Another step in the RAG pipeline could validate the results?

## To Do
 - [ ] Refine the  Flesch-Kincaid Grade Level <> Reading Age lookup
 - [ ] Improve the prompt
 - [ ] Right now, only text is handled. Docx and PDF would be preferable for an education setting. 

 ##  Requirements
 * Bash (or similar)
 * OpenAPI API key

 ##  Installation
 1. Pull the git repo
 2. Change directory to the demo
 3. Activate `make activate`
 4. Install dependencies `make install`
 5. Copy `apikey.example.py` to `apikey.py` and enter your OpenAPI API key
 6. Run `make serve`