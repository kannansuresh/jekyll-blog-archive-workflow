FROM python:3

ADD dist/_create-archive-files.py /

RUN pip install -Iv requests

CMD ["python", "/dist/_create-archive-files.py"]