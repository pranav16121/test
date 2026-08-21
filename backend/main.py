from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from . import items
from .supabase_client import supabase


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


class StatusUpdate(BaseModel):
    status: str = Field(..., description="active, resolved, or Returned")


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
        raise HTTPException(status_code=400, detail="Status must be 'active', 'resolved', or 'Returned'.")
    return value


def _serialize_item(record: dict) -> dict:
    output = dict(record)
    if "name" not in output:
        output["name"] = output.get("title", "")
    if output.get("type"):
        output["type"] = str(output["type"]).capitalize()
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
    item = items.create_item(
        supabase=supabase,
        item_type=_normalize_type(payload.type),
        title=payload.name.strip(),
        description=(payload.description or "").strip(),
        location=payload.location.strip(),
    )
    return _serialize_item(item)


@app.get("/items/")
def get_items(query: Optional[str] = None):
    _require_supabase()
    records = items.fetch_items(supabase=supabase, search_query=query)
    return [_serialize_item(record) for record in records]


@app.patch("/items/{item_id}/status")
def update_item_status(item_id: int, payload: StatusUpdate):
    _require_supabase()
    updated = items.update_item_status(
        supabase=supabase,
        item_id=item_id,
        status=_normalize_status(payload.status),
    )
    if not updated:
        raise HTTPException(status_code=404, detail=f"Item with ID {item_id} not found.")
    return _serialize_item(updated)
