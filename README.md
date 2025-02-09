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

### Shorten a URL (with Rate Limiting)
- **Endpoint:** `POST /api/v1/shorten/`
- **Rate Limit:** 1 request per minute per IP
- **Payload:**
```json
{
  "long_url": "https://example.com"
}
```
- **Response:**
```json
{
    "status_code": 200,
    "message": "Okay.",
    "data": {
        "short_url": "http://short.ner/s1qbl8"
    },
    "success": true
}
```

### List All Shortened URLs (with Rate Limiting)
- **Endpoint:** `GET /api/v1/shortened-urls/`
- **Rate Limit:** 1 request per minute per IP
- **Response:**
```json
{
    "status_code": 200,
    "message": "Okay.",
    "data": [
        {
            "id": 1,
            "short_url": "http://short.ner/s1qbl8",
            "created_at": "2025-02-09T19:10:16.012311Z",
            "updated_at": "2025-02-09T19:10:16.012365Z",
            "long_url": "http://127.0.0.1:8000/api/v2/shorten/",
            "short_code": "s1qbl8"
        },
        {
            "id": 2,
            "short_url": "http://short.ner/egjdq6",
            "created_at": "2025-02-09T19:19:05.706349Z",
            "updated_at": "2025-02-09T19:19:05.706432Z",
            "long_url": "http://127.0.0.1:8000/api/v3/shorten/",
            "short_code": "egjdq6"
        }
    ],
    "success": true
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
