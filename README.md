# Email Sending Service

## Setup and Run

1. Copy `.env.example` to `.env` and fill in credentials.
2. Create venv:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install:
   ```bash
   pip install -r requirements.txt
   ```
4. Start service:
   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
   ```

Paths:
```
$PWD
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── README.md
├── app/
└── tests/
```
