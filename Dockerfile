FROM python:3.7.2-alpine3.8

RUN adduser -D crawler
WORKDIR /home/crawler

COPY . .
RUN apk add --update --no-cache g++ gcc libxslt-dev==1.1.32-r0
RUN pip install -r requirements.txt
RUN apk del g++ gcc
USER crawler
EXPOSE 8000
CMD ["gunicorn","--bind","0.0.0.0:8000","wsgi"]
