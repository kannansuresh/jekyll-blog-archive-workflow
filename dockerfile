FROM python:3

RUN pip install -Iv requests

ENTRYPOINT ["python", "dist/_create-archive-files.py"]