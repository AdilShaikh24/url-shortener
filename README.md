# DRF URL Shortener

## Overview
This project is a simple URL shortener built using Django Rest Framework (DRF). It allows users to submit a long URL and receive a shortened version. When the shortened URL is accessed, it redirects to the original long URL.

## Features
- Shorten long URLs
- Redirect to original URLs using short codes
- Rate limiting (10 requests per minute per IP)
- Unit tests for core functionality
- Docker support for containerized deployment

## Requirements
- Python 3.9+
- Django
- Django REST Framework
- SQLite 
- Docker & Docker Compose

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/url-shortener.git
cd url-shortener
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations w/o docker
```bash
python manage.py migrate
```

### 5. Run the Development Server w/o docker
```bash
python manage.py runserver
```

## Usage

### Shorten a URL
- **Endpoint:** `POST /api/v1/shorten/`
- **Payload:**
```json
{
  "long_url": "https://example.com"
}
```
- **Response:**
```json
{
  "short_url": "http://short.ner/abc123"
}
```

### Redirect to Original URL
- **Endpoint:** `GET /api/v1/<short_code>/`
- Redirects to the original long URL.

## Running Tests
```bash
python manage.py test apps/urlshortener/tests
```

## Docker Setup
### Build and Run the Container
```bash
docker-compose up --build
```
This will start the Django app.
