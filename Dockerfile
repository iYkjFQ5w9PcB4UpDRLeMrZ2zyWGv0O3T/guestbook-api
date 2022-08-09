FROM python:3.6-slim-stretch

WORKDIR /app
RUN pip3 install --upgrade pip setuptools

ADD requirements.txt requirements.txt

ADD main.py main.py

RUN pip install -r requirements.txt

ADD app app
RUN python3 -m spacy download en \
    && python3 -m spacy download fr \
    && python3 -m spacy download pt \
    && python3 -m spacy download de \
    && python3 -m spacy download es \
    && python3 -m spacy download it_core_news_sm
    
EXPOSE 8080

CMD ["python", "main.py"]
