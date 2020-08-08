FROM python:3

RUN pip install -Iv requests

COPY ./ /generatedocs

ENTRYPOINT ["python", "/generatedocs/dist/_create-archive-files.py"]