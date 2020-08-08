FROM python:3

RUN pip install -Iv requests

COPY ./ /generatearchiviefiles

ENTRYPOINT ["python", "/generatearchiviefiles/dist/_create-archive-files.py"]