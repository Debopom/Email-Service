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

## Run

```bash
uvicorn app.main:app --reload
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
