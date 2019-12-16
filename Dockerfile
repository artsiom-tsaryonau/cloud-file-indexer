FROM python:3

COPY credentials.json /home/tmp

RUN pip install mega.py
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

CMD ["python", "/home/tmp/script.py"]
