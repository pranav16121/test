import sys
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from postgrest.exceptions import APIError

# Ensure current directory is in sys.path for direct execution
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from . import items
    from .supabase_client import supabase
except (ImportError, ValueError):
    import items
    from supabase_client import supabase


app = FastAPI(title="Lost & Found API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ItemCreate(BaseModel):
    type: str = Field(..., description="Lost or Found")
    name: str = Field(..., min_length=1)
    description: Optional[str] = ""
    location: str = Field(..., min_length=1)
    category: Optional[str] = "General"
    date: Optional[str] = None
    contact_email: Optional[str] = None
    image: Optional[str] = None


class StatusUpdate(BaseModel):
    status: str = Field(..., description="Active or Returned")


def _normalize_type(item_type: str) -> str:
    value = item_type.strip().lower()
    if value not in {"lost", "found"}:
        raise HTTPException(status_code=400, detail="Type must be either 'Lost' or 'Found'.")
    return value


def _normalize_status(item_status: str) -> str:
    value = item_status.strip().lower()
    if value == "returned":
        value = "resolved"
    if value not in {"active", "resolved"}:
        raise HTTPException(status_code=400, detail="Status must be 'Active' or 'Returned'.")
    return value


def _serialize_item(record: dict) -> dict:
    output = dict(record)
    if "name" not in output:
        output["name"] = output.get("title", "")
    if output.get("type"):
        output["type"] = str(output["type"]).capitalize()
    if output.get("status"):
        status_value = str(output["status"]).strip().lower()
        if status_value == "active":
            output["status"] = "Active"
        elif status_value in {"returned", "resolved"}:
            output["status"] = "Returned"
    return output


def _require_supabase() -> None:
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client is not initialized. Check SUPABASE_URL and SUPABASE_KEY.",
        )


@app.post("/items/", status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate):
    _require_supabase()
    try:
        item = items.create_item(
            supabase=supabase,
            item_type=_normalize_type(payload.type),
            title=payload.name.strip(),
            description=(payload.description or "").strip(),
            location=payload.location.strip(),
            category=(payload.category or "General").strip(),
            date=payload.date,
            contact_email=payload.contact_email,
            image=payload.image,
        )
    except APIError as exc:
        raise HTTPException(status_code=503, detail=f"Supabase database error: {exc.message}") from exc
    return _serialize_item(item)


@app.get("/items/")
def get_items(query: Optional[str] = None):
    _require_supabase()
    try:
        records = items.fetch_items(supabase=supabase, search_query=query)
    except APIError as exc:
        raise HTTPException(status_code=503, detail=f"Supabase database error: {exc.message}") from exc
    return [_serialize_item(record) for record in records]


@app.patch("/items/{item_id}/status")
def update_item_status(item_id: int, payload: StatusUpdate):
    _require_supabase()
    try:
        updated = items.update_item_status(
            supabase=supabase,
            item_id=item_id,
            status=_normalize_status(payload.status),
        )
    except APIError as exc:
        raise HTTPException(status_code=503, detail=f"Supabase database error: {exc.message}") from exc
    if not updated:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found.")
    return _serialize_item(updated)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
