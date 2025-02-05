from fastapi import APIRouter, HTTPException
from services.database import get_collection, serialize_documents
from models import Interaction, PyObjectId

router = APIRouter()

@router.post("/record")
async def record_interaction(interaction: Interaction):
    collection = get_collection("interactions")
    result = collection.insert_one(interaction.dict())
    return {"id": str(result.inserted_id), "message": "Interaction recorded"}


@router.get("/interactionss/{lead_id}")
async def get_contacts(lead_id: str):
    # No need for ObjectId conversion if lead_id is stored as a string
    interactions_collection = get_collection("interactions")
    
    # Directly querying the lead_id as a string
    contacts = interactions_collection.find({"lead_id": lead_id})

    contact_list = [
        {
            "_id": str(contact["_id"]),
            "lead_id": contact["lead_id"],
            "type": contact.get("type"),
            "details": contact.get("details"),
            "date": contact.get("date")
        }
        for contact in contacts
    ]

    if not contact_list:
        raise HTTPException(status_code=404, detail="No contacts found for the given lead_id")

    return {"contacts": contact_list}

