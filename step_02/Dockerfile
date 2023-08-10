FROM python:3.9-slim-bullseye
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8010
COPY . .
CMD ["streamlit", "run", "PEA_power_flow.py", "--server.port", "8080", "--server.address", "0.0.0.0"]