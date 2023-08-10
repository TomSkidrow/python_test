FROM python:3.9-slim-bullseye
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["streamlit", "run", "./evDummy.py", "--server.port", "8000", "--server.address", "0.0.0.0"]