# Test Differentiator By Reading Age Test
## About
* This demo takes some sample text (by default a section from the [https://www.hoddereducation.com/media/resources/he/Geography/A-level/9781471858703/OCR-A-level-Geography-sample-chapter.pdf](Hodder OCR Geography A Level textbook on human rights)).
* It then uses Chat GPT to attempt to differentiate the work for the selected reading ages. 
* The content returned from ChatGPT is then checked against the Flesch Kincaid_grade.
    * This is then roughly converted to a "reading age"
* If the returned text doesn't match the absolute value of the target reading age, the request is re-run. 
    * This happens 3 times
    * If no exact match is found, then the best of 3 is taken
* Finally, the "best of 3" result is sent to Chat GPT to check for British English spelling, punctuation and grammar. 

## To Do
 - [ ] Refine the  Flesch-Kincaid Grade Level <> Reading Age lookup
