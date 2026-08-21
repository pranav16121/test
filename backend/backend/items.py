from typing import List, Optional
from datetime import date
from supabase import Client

def create_item(
    supabase: Client,
    item_type: str,
    title: str,
    description: Optional[str],
    category: str,
    location: str,
    item_date: str,
    image_url: Optional[str],
    contact_email: str
) -> Optional[dict]:
    """
    Inserts a new item into the 'lost_found_items' table in Supabase.
    """
    if not supabase:
        raise ValueError("Supabase client is not initialized.")
        
    data = {
        "type": item_type,
        "title": title,
        "description": description,
        "category": category,
        "location": location,
        "date": item_date,
        "image": image_url,
        "contact_email": contact_email,
        "status": "active"
    }
    
    response = supabase.table("lost_found_items").insert(data).execute()
    return response.data[0] if response.data else None


def fetch_items(
    supabase: Client,
    item_type: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    search_query: Optional[str] = None
) -> List[dict]:
    """
    Fetches items from Supabase with optional filters.
    """
    if not supabase:
        raise ValueError("Supabase client is not initialized.")
        
    query_builder = supabase.table("lost_found_items").select("*")
    
    if item_type:
        query_builder = query_builder.eq("type", item_type)
    if category:
        query_builder = query_builder.eq("category", category)
    if status:
        query_builder = query_builder.eq("status", status)
        
    if search_query:
        # Search query checks if title or description contains the search string (case insensitive)
        query_builder = query_builder.or_(f"title.ilike.%{search_query}%,description.ilike.%{search_query}%")
        
    response = query_builder.order("created_at", descending=True).execute()
    return response.data


def update_item_status(
    supabase: Client,
    item_id: int,
    status: str
) -> Optional[dict]:
    """
    Updates the status of an item (e.g. to 'resolved').
    """
    if not supabase:
        raise ValueError("Supabase client is not initialized.")
        
    if status not in ["active", "resolved"]:
        raise ValueError("Status must be either 'active' or 'resolved'.")
        
    response = supabase.table("lost_found_items").update({"status": status}).eq("id", item_id).execute()
    return response.data[0] if response.data else None
