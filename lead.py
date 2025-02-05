import logging
from typing import Collection
from fastapi import APIRouter, HTTPException
from services.database import get_collection
from models import Lead, PyObjectId

router = APIRouter()

@router.post("/add")
async def add_lead(lead: Lead):
    collection = get_collection("leads")
    result = collection.insert_one(lead.dict(by_alias=True))
    return {"id": str(result.inserted_id), "message": "Lead added successfully"}


@router.get("/getlead/{lead_id}")
async def get_contacts(lead_id: str):
    lead_collection: Collection = get_collection("leads")
    
    # Debugging: Log the lead_id received from the request
    logging.debug(f"Received lead_id: {lead_id}")
    
    # Check if lead_id is a valid ObjectId and convert it, if necessary
    if len(lead_id) == 24 and all(c in '0123456789abcdef' for c in lead_id.lower()):
        # If it's a valid ObjectId (24-character hex string), convert it
        lead_id = PyObjectId(lead_id)
        query = {"_id": lead_id}  # Query by _id if it's an ObjectId
    else:
        # If lead_id is not an ObjectId, query by lead_id field (assuming it's stored as a string)
        query = {"lead_id": lead_id}  # Query by the lead_id field
    
    # Debugging: Log the actual query being sent to the database
    logging.debug(f"Querying with query: {query}")

    # Fetch the leads from the collection
    leads = lead_collection.find(query)
    
    # Debugging: Log the raw data returned by the query
    leads_list = list(leads)
    logging.debug(f"Leads found: {leads_list}")
    
    # Process the results into a list of lead information
    lead_list = [
        {
            "_id": str(contact["_id"]),
            "status": contact.get("status"),
            "name": contact.get("name"),
            "email": contact.get("email"),
            "phone": contact.get("phone"),
            "requirement": contact.get("requirements"),
            "last Call": contact.get("last_called"),
        }
        for contact in leads_list
    ]
    
    # If no leads are found, raise a 404 error
    if not lead_list:
        raise HTTPException(status_code=404, detail="No contacts found for the given lead_id")
    
    return {"contacts": lead_list}
@router.get("/{lead_id}")
async def get_lead_status(lead_id: str):
    collection = get_collection("leads")
    lead = collection.find_one({"_id": PyObjectId(lead_id)})
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"status": lead["status"]}

@router.put("/{lead_id}")
async def update_lead_status(lead_id: str, status: str):
    collection = get_collection("leads")
    result = collection.update_one({"_id": PyObjectId(lead_id)}, {"$set": {"status": status}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Lead status updated"}
