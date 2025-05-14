# Email Microservice

A simple internal FastAPI-based microservice for sending transactional emails via SMTP.


## Prerequisites

* Python 3.8+
* Access to an SMTP server (e.g., Gmail with App Password)

## Project Structure

```
email_service/
├── .env               # SMTP and logging settings
├── requirements.txt   # Python dependencies
├── config.py          # Environment loader
├── schemas.py         # Pydantic models
├── email_sender.py    # SMTP logic
└── main.py            # FastAPI app definition
```

## Setup

1. **Clone or copy** the project into `~/email_service`:

   ```bash
   mkdir -p ~/email_service && cd ~/email_service
   # copy files here
   ```

2. **Create and activate** a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure** your SMTP settings in `.env`:

   ```ini
   SMTP_HOST=<your.smtp.server>
   SMTP_PORT=587
   SMTP_USER=you@gmail.com
   SMTP_PASSWORD=<your_app_password>
   SMTP_USE_TLS=True
   LOG_FILE=email_service.log
   ```

## Running the Service

With your venv active:

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

* The API will be available at `http://127.0.0.1:8000`.
* All requests outside of `127.0.0.1`/`::1` will be rejected with `403 Forbidden`.

## Usage Example

Send a basic email:

```bash
curl -X POST http://127.0.0.1:8000/send-email \
  -H "Content-Type: application/json" \
  -d '{
        "to": ["alice@example.com","bob@example.com"],
        "subject": "Test Email",
        "body": "<b>Hello to test!</b>"
      }'
```

Send with attachment:

```bash
# create a file
echo "Test content" > test.txt

curl -X POST http://127.0.0.1:8000/send-email \
  -H "Content-Type: application/json" \
  -d '{
        "to": "you@gmail.com",
        "subject": "With Attachment",
        "body": "Please see attached",
        "attachments": ["./test.txt"]
      }'
```

## Logs

All activity and errors are logged to the file specified by `LOG_FILE` (default `email_service.log`).

```bash
tail -f email_service.log
```

## Troubleshooting

* **DNS errors**: Ensure `SMTP_HOST` is correct (e.g., `smtp.gmail.com`).
* **Authentication errors**: Use a valid App Password for Gmail and ensure 2FA is enabled.
* **Forbidden**: Confirm you’re sending requests from `127.0.0.1`.
