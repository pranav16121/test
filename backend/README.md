# Lost & Found Backend (FastAPI + Supabase)

## Files
- `backend/main.py` – FastAPI routes
- `backend/items.py` – Supabase table operations
- `backend/supabase_client.py` – Supabase client init from env vars
- `backend/test_backend.py` – API tests (mocked)

## Required environment variables
Create `/home/runner/work/test/test/backend/.env`:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
```

Optional (not required for this MVP):
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`

## Install
From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## Run backend
From repository root:

```bash
uvicorn backend.main:app --reload
```

Swagger docs:
- `http://127.0.0.1:8000/docs`

## API endpoints
- `POST /items/`
- `GET /items/`
- `PATCH /items/{item_id}/status`

`GET /items/?query=...` performs search.

## Supabase table
Use table name: `lost_found_items`.

Minimum expected columns used by this MVP:
- `id` (primary key)
- `type` (`lost`/`found`)
- `title`
- `description`
- `location`
- `status` (`active`/`resolved`)
- `category`
- `date`
- `contact_email`
- `created_at`

## Tests
From repository root:

```bash
python -m unittest backend/test_backend.py
```
