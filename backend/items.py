from datetime import date
from typing import Optional

from supabase import Client


TABLE_NAME = "lost_found_items"


def create_item(
    supabase: Client,
    item_type: str,
    title: str,
    description: str,
    location: str,
) -> dict:
    data = {
        "type": item_type,
        "title": title,
        "description": description,
        "location": location,
        "status": "active",
        "category": "General",
        "date": date.today().isoformat(),
        "contact_email": "unknown@example.com",
    }
    response = supabase.table(TABLE_NAME).insert(data).execute()
    return response.data[0]


def fetch_items(supabase: Client, search_query: Optional[str] = None) -> list[dict]:
    query = supabase.table(TABLE_NAME).select("*").order("created_at", desc=True)
    if search_query:
        query_text = search_query.strip()
        query = query.or_(
            f"title.ilike.%{query_text}%,description.ilike.%{query_text}%,location.ilike.%{query_text}%"
        )
    response = query.execute()
    return response.data or []


def update_item_status(supabase: Client, item_id: int, status: str) -> Optional[dict]:
    response = supabase.table(TABLE_NAME).update({"status": status}).eq("id", item_id).execute()
    if not response.data:
        return None
    return response.data[0]
