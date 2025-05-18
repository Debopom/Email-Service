# Email Sending Service

A simple microservice to send emails via SMTP.

## Setup

1. Copy `.env.example` to `.env` and update with your SMTP credentials.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the API

In one terminal, start FastAPI:

```bash
uvicorn app.main:app --reload
```

## Start Redis

Make sure Redis is running:

```bash
redis-cli ping   # responds PONG
```

> *If Redis isn't installed, install via `sudo apt install redis-server` and start with `sudo service redis-server start`.*

## Start Celery Worker

In a second terminal (with virtualenv active), launch Celery:

```bash
celery -A app.core.celery:celery_app worker --loglevel=info
```


## Send Email (Plain Text or HTML Body)

POST `/api/v1/send` with JSON body:

```json
{
  "to": "user@example.com",
  "subject": "Test Email",
  "body": "Hello world!"
}
```

## Send Email with Template

If you have an email template in `app/templates/`, include `template_name` and optional `template_data`:

```json
{
  "to": "user@example.com",
  "subject": "Welcome!",
  "template_name": "account_creation.html",
  "template_data": {
    "username": "Alice",
    "site_name": "MyApp",
    "activation_link": "https://myapp.com/activate/abc123"
  }
}
```

This will render the specified Jinja2 template and send it as HTML email. Modify `template_data` keys to match your template placeholders.
