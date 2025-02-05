from fastapi import APIRouter, HTTPException
from services.database import get_collection
from models import Contact, PyObjectId

router = APIRouter()

@router.post("/add")
async def add_contact(contact: Contact):
    collection = get_collection("contacts")
    result = collection.insert_one(contact.dict())
    return {"id": str(result.inserted_id), "message": "Contact added successfully"}

@router.get("/get")
async def get_contacts(lead_id: str):
    # No need for ObjectId conversion if lead_id is stored as a string
    contacts_collection = get_collection("contacts")
    
    # Directly querying the lead_id as a string
    contacts = contacts_collection.find({"lead_id": lead_id})

    contact_list = [
        {
            "_id": str(contact["_id"]),
            "lead_id": contact["lead_id"],
            "name": contact.get("contact_name"),
            "role": contact.get("contact_role"),
            "phone": contact.get("phone")
        }
        for contact in contacts
    ]

    if not contact_list:
        raise HTTPException(status_code=404, detail="No contacts found for the given lead_id")

    return {"contacts": contact_list}

