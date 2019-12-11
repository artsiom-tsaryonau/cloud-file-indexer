FROM python:3

RUN pip install mega.py

CMD ["python", "/home/tmp/script.py"]
