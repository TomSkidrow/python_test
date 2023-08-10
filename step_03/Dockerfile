FROM python:3.9-slim-bullseye
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
EXPOSE 9000
EXPOSE 8080
COPY . .
CMD ["/bin/bash", "-c", "./startup.sh"]