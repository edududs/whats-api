## whats-api

A small Python client to interact with the Evolution API (WhatsApp) for fetching chats/messages and sending text.

### Requirements

- Python 3.13
- `uv` for dependency management (`pipx install uv`), or use `pip`
- Docker and Docker Compose (to run Evolution API locally)

### Setup

1. Install dependencies:
   - With uv: `uv sync`
   - For development extras: `uv sync --extra dev`
2. Create your environment file:
   - Copy `env.example` to `.env` and adjust the values as needed
3. (Optional) Start the Evolution API locally:
   - `docker compose up -d`

### Environment Variables

- `AUTHENTICATION_API_KEY`: API key for Evolution API
- `EVO_URL`: Base URL for Evolution API (e.g., http://localhost:8080)
- `EVO_INSTANCE`: Instance name (e.g., carpool)

### Usage

Run the main script:
