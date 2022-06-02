FROM python:3.8.6-buster

COPY predict.py /predict.py
COPY requirements.txt /requirements.txt
COPY TaxiFareModel /TaxiFareModel
COPY api /api
COPY model.joblib /model.joblib
COPY Makefile /Makefile

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD make run_api_prod