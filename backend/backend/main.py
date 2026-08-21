import os
import shutil
import uuid
from datetime import datetime, date
from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

from .supabase_client import supabase
from . import items

load_dotenv()

app = FastAPI(
    title="College Lost and Found Backend API",
    description="FastAPI Backend aligned with Tkinter Frontend and Supabase",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cloudinary configuration
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

use_cloudinary = all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET])

if use_cloudinary:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True
    )

# Local fallback directory for image uploads
UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Mount static folder (used if Cloudinary credentials are not set)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Pydantic Schemas for Validation
class ItemCreate(BaseModel):
    type: str = Field(..., description="Must be 'lost' or 'found'")
    title: Optional[str] = None
    name: Optional[str] = None  # Fallback: maps frontend 'name' to 'title'
    description: Optional[str] = None
    category: Optional[str] = "Others"  # Default fallback if frontend doesn't supply it
    location: str
    date: Optional[str] = None  # Fallback: defaults to current date if missing
    image: Optional[str] = None
    contact_email: Optional[str] = "anonymous@college.edu"  # Default fallback

class StatusUpdate(BaseModel):
    status: str = Field(..., description="Must be 'active', 'resolved', or 'returned'")


@app.post("/items/", status_code=status.HTTP_201_CREATED)
def add_item(item_in: ItemCreate):
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client is not initialized. Please verify SUPABASE_URL and SUPABASE_KEY."
        )
        
    # Align 'name' from frontend to 'title'
    item_title = item_in.title or item_in.name
    if not item_title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item 'title' or 'name' is required."
        )
        
    # Standardize type to lowercase
    item_type = item_in.type.lower()
    if item_type not in ["lost", "found"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Type must be either 'lost' or 'found'"
        )
        
    # Default to current date if not provided
    item_date = item_in.date or date.today().isoformat()
    
    try:
        new_item = items.create_item(
            supabase=supabase,
            item_type=item_type,
            title=item_title,
            description=item_in.description,
            category=item_in.category,
            location=item_in.location,
            item_date=item_date,
            image_url=item_in.image,
            contact_email=item_in.contact_email
        )
        if not new_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not insert item record."
            )
        return new_item
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.get("/items/")
def list_items(
    type: Optional[str] = None,
    category: Optional[str] = None,
    status: Optional[str] = None,
    query: Optional[str] = None
):
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client is not initialized. Please verify SUPABASE_URL and SUPABASE_KEY."
        )
        
    # Lowercase filter inputs for safety
    item_type = type.lower() if type else None
    item_status = status.lower() if status else None
    
    # Map 'returned' to 'resolved' in queries
    if item_status == "returned":
        item_status = "resolved"
        
    try:
        records = items.fetch_items(
            supabase=supabase,
            item_type=item_type,
            category=category,
            status=item_status,
            search_query=query
        )
        return records
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.patch("/items/{item_id}/status")
def patch_item_status(item_id: int, status_update: StatusUpdate):
    if not supabase:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Supabase client is not initialized. Please verify SUPABASE_URL and SUPABASE_KEY."
        )
        
    # Standardize status to lowercase and map 'returned' to 'resolved'
    target_status = status_update.status.lower()
    if target_status == "returned":
        target_status = "resolved"
        
    if target_status not in ["active", "resolved"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status must be 'active', 'resolved', or 'returned'"
        )
        
    try:
        updated_item = items.update_item_status(
            supabase=supabase,
            item_id=item_id,
            status=target_status
        )
        if not updated_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found."
            )
        return updated_item
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@app.post("/items/upload-image/")
def upload_image(file: UploadFile = File(...)):
    # Validate extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".jpg", ".jpeg", ".png", ".gif", ".webp"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image format. Allowed formats: JPG, JPEG, PNG, GIF, WEBP."
        )
        
    if use_cloudinary:
        try:
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                file.file,
                folder="college_lost_and_found"
            )
            return {"image_url": upload_result.get("secure_url")}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Cloudinary upload failed: {str(e)}"
            )
    else:
        # Fallback to local storage if Cloudinary is not configured
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        relative_url = f"/static/uploads/{unique_filename}"
        return {"image_url": relative_url}
