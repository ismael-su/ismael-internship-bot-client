FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN  pip install poetry numpy datasets transformers torch python-socketio asyncio aiohttp

EXPOSE 8000
COPY . /app

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0","--port","8000"]
