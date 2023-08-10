FROM python:3.9-slim-bullseye
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
CMD ["streamlit", "run", "PEA_cpo_eff.py", "--server.port", "8080", "--server.address", "0.0.0.0"]