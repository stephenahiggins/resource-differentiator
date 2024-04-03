activate:
	source ./bin/activate
install: 
	pip3 install -r requirements.txt
deactivate:
	deactivate
freeze: 
	pip freeze > requirements.txt
check-deps:
	creosote --venv ./ --path ./src --deps-file ./requirements.txt
serve:
	streamlit run ./src/differentiator.py