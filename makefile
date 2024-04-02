activate:
	source ./bin/activate
deactivate:
	deactivate
freeze: 
	pip freeze > requirements.txt
check-deps:
	creosote --venv ./ --path ./src --deps-file ./requirements.txt
serve:
	streamlit run ./src/differentiator.py