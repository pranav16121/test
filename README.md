# Lost & Found MVP

Tkinter frontend + FastAPI backend + Supabase database.

## Project structure

```text
frontend/Frontend.py
backend/main.py
backend/items.py
backend/supabase_client.py
backend/requirements.txt
backend/.env.example
backend/.gitignore
backend/README.md
backend/test_backend.py
README.md
.gitignore
```

## 1) Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## 2) Install dependencies

```bash
pip install -r backend/requirements.txt
```

## 3) Create backend env file

Create `/home/runner/work/test/test/backend/.env`:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
```

Cloudinary variables are optional for this MVP.

## 4) Run backend

From repo root:

```bash
uvicorn backend.main:app --reload
```

Swagger docs:
- `http://127.0.0.1:8000/docs`

## 5) Run frontend

In another terminal (same repo root):

```bash
python frontend/Frontend.py
```

Optional frontend backend URL override:

```bash
BACKEND_URL=http://127.0.0.1:8000 python frontend/Frontend.py
```

## Supabase setup still required
- Create a Supabase project.
- Create a `lost_found_items` table with columns expected in `backend/README.md`.
- Put valid `SUPABASE_URL` and `SUPABASE_KEY` in `backend/.env`.
