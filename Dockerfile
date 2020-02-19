FROM python:3.8-alpine
ENV PYTHONBUFFERED 1
WORKDIR /code
COPY . .
EXPOSE 8000
CMD python -m converter --host 0.0.0.0 --port 8000
