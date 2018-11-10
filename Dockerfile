FROM python:3
WORKDIR /usr/src/app
ADD requirements.txt ./
RUN pip install -r requirements.txt
ADD src/ ./src
ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"
