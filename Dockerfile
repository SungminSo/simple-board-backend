FROM python:3.8-slim-buster

ADD . /board

WORKDIR /board

RUN pip install --upgrade pip ; \
	pip install pipenv
RUN pipenv install --system --dev

ENV USER_JWT_SECRET_KEY "qwerasdfzxcv1234"

EXPOSE 5000

CMD ["python", "./manage.py", "run"]
