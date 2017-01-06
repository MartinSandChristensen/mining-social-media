FROM pyservice

RUN pip install nltk # An up to date version? Yes, please.
RUN pip install pika

ADD tweetparser.py .

ENTRYPOINT ["python", "tweetparser.py"]
