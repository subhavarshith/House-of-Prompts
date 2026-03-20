# Stage 1: Build the React frontend
FROM node:20 AS frontend-build
WORKDIR /app/frontend
COPY Pulse-Guard/frontend/package*.json ./
RUN npm install
COPY Pulse-Guard/frontend/ ./
RUN npm run build

# Stage 2: Build the FastAPI backend
FROM python:3.11-slim
WORKDIR /app

COPY Pulse-Guard/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Pulse-Guard/backend/ ./backend/
COPY --from=frontend-build /app/frontend/dist/ ./backend/static/

# Bake the API key into the container so the user doesn't have to configure secrets in Cloud Run MVP
ENV GEMINI_API_KEY=AIzaSyCS2HLhIvEReRmigQoVf9WXFEZXaS6zQZ4
ENV PORT=8080
EXPOSE 8080

WORKDIR /app/backend
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}
