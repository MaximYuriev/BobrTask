FROM python:3.12

RUN mkdir /bobr_app

WORKDIR /bobr_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD python main.py