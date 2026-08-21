Testing prep 
Pranav
sriram
# test
Testing prep 
Pranav
sriram

# Lost & Found MVP

Tkinter frontend + FastAPI backend + Supabase database.

## Install dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r backend/requirements.txt
```

## Configure Supabase

Create `backend/.env` and add the real project values locally. Keep this file
out of Git; real credentials must not be placed in source code or documentation.

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
```

In the Supabase SQL Editor, run `backend/schema.sql` once to create the
`lost_found_items` table and its anonymous read/insert/update policies. The
script uses `if not exists` checks and does not delete or reset data.

## Start the backend

```bash
python -m uvicorn backend.main:app --reload
```

Open <http://127.0.0.1:8000/docs> for the FastAPI documentation.

## Start the frontend

In a second terminal, from the project root:

```bash
python frontend/Frontend.py
```

The frontend loads and updates `lost_found_items` through the API. Existing
rows using `active`/`resolved` are shown as `Active`/`Returned`.
