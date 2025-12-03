
FROM python:3.11-slim


WORKDIR /app


ENV PYTHONPATH "${PYTHONPATH}:/app/src" 


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ /app/src/


RUN mkdir -p /app/data


EXPOSE 8000


CMD ["uvicorn", "turkey_twin.api:app", "--host", "0.0.0.0", "--port", "8000"]