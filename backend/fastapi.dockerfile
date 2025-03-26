FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 


COPY . ./

EXPOSE 8000

ENV FASTAPI_ENV=development
ENV DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
ENV FASTAPI_DEBUG=1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

