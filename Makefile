install:
	python -m pip install -r requirements.txt

test:
	pytest -q

lint:
	flake8 app tests main.py

run:
	flask --app main run --debug

docker-up:
	docker compose up --build

docker-down:
	docker compose down

backup:
	./scripts/backup.sh
