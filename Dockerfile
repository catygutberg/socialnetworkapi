FROM python:3.9-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PATH="/home/djangouser/.local/bin:${PATH}" \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update &&\
    apt-get -y install python3-psycopg2 &&\
    useradd -m djangouser

USER djangouser

WORKDIR /home/djangouser

COPY --chown=djangouser:djangouser requirements.txt requirements.txt
RUN pip install --no-cache-dir --user -r requirements.txt

COPY --chown=djangouser:djangouser manage.py manage.py
COPY --chown=djangouser:djangouser socialnetwork socialnetwork
COPY --chown=djangouser:djangouser api api

CMD ["python", "./manage.py", "runserver", "0.0.0.0:${PORT}"]
