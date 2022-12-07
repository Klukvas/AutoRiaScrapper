# syntax=docker/dockerfile:1
FROM python:3.10.5-slim-buster
ENV SECRET_KEY=OIA7RnkjCpm5zuq9
ENV FLASK_ENV=development
EXPOSE 5001
# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN pip install aiohttp
RUN apt-get update && apt-get install -y --no-install-recommends gcc
# Install python dependencies in /.venv
COPY . ./app
#RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
RUN pipenv lock
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install aiohttp
#CMD ["pipenv", "run", "python", "manage.py", "runserver"]