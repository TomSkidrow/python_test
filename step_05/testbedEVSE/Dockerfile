FROM python:3.9-slim-bullseye
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
EXPOSE 8001
COPY . .
CMD ["uvicorn", "evseDummy:app", "--host", "0.0.0.0", "--port", "8000"]