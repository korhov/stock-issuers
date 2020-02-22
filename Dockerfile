FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /home/stock-issuers

WORKDIR /home/stock-issuers

COPY . /home/stock-issuers/

RUN pip install --upgrade pip \
 && pip install -r requirements.txt

EXPOSE  80
CMD ["python", "./api.py"]