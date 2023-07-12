
run:
	python3.10 main.py
test:
	python3.10 -m unittest discover -p "*.py"
freeze:
	pip3 freeze > requirements.txt
install:
	pip3 install -r requirements.txt

# source ./venv/bin/activate
# deactive
