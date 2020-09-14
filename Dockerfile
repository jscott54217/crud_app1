FROM python:3.7
WORKDIR /usr/src/app

RUN python -m pip install \
        pandas

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .
CMD ["python", "app.py"]