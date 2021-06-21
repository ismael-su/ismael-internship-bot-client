FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN  pip install  poetry

EXPOSE 8000
COPY . /
RUN ls -la /
RUN poetry install

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0","--port","8000"]
