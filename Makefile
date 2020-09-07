install:
	pipenv install

install-dev:
	pipenv install --dev

run:
	python3 manage.py run

migrate:
	python3 manage.py db migrate
	python3 manage.py db upgrade

docker:
	docker build -t simple-board .
	docker-compose up