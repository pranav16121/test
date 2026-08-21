import datetime
from typing import Optional

from supabase import Client


TABLE_NAME = "lost_found_items"


def create_item(
    supabase: Client,
    item_type: str,
    title: str,
    description: str,
    location: str,
    category: Optional[str] = None,
    date: Optional[str] = None,
    contact_email: Optional[str] = None,
    image: Optional[str] = None,
) -> dict:
    data = {
        "type": item_type,
        "title": title,
        "description": description,
        "location": location,
        "category": category or "General",
        "date": date or str(datetime.date.today()),
        "contact_email": contact_email or "anonymous@lostfound.local",
        "status": "active",
    }
    if image is not None:
        data["image"] = image
    response = supabase.table(TABLE_NAME).insert(data).execute()
    if not response.data:
        raise RuntimeError("Supabase did not return the created item.")
    return response.data[0]


def fetch_items(supabase: Client, search_query: Optional[str] = None) -> list[dict]:
    query = supabase.table(TABLE_NAME).select("*").order("created_at", desc=True)
    if search_query and search_query.strip():
        query_text = search_query.strip().replace(",", "")
        query = query.or_(
            f"title.ilike.%{query_text}%,description.ilike.%{query_text}%,location.ilike.%{query_text}%,category.ilike.%{query_text}%"
        )
    response = query.execute()
    return response.data or []


def update_item_status(supabase: Client, item_id: int, status: str) -> Optional[dict]:
    response = (
        supabase.table(TABLE_NAME)
        .update({"status": status})
        .eq("id", item_id)
        .execute()
    )
    return response.data[0] if response.data else None
