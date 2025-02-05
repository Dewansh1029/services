from fastapi import APIRouter, HTTPException
from services.database import get_collection, serialize_documents
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/todays")
async def get_today_call():
    collection = get_collection("call_frequency")
    today = datetime.now()
    leads = list(
        collection.find({
            "$or": [
                {"last_called": None},
                {"last_called": {"$lt": (today - timedelta(days=7)).isoformat()}}
            ]
        })
    )
    return serialize_documents(leads)  # Serialize the documents before returning


@router.post("/call_planninge/")
async def create_call_entry(frequency: int):
    leads_collection = get_collection("leads")
    calls_collection = get_collection("call_planning")

    # Fetch the latest lead_id from the leads collection
    latest_lead = leads_collection.find_one(sort=[("_id", -1)])
    
    if not latest_lead:
        raise HTTPException(status_code=404, detail="No leads found to create a call entry.")
    
    lead_id = latest_lead["lead_id"]

    # Insert call entry with auto-fetched lead_id
    call_entry = {
        "lead_id": lead_id,
        "frequency": frequency,
        "last_called": None
    }

    result = calls_collection.insert_one(call_entry)
    return {
        "id": str(result.inserted_id),
        "message": "Call entry created successfully",
        "lead_id": lead_id
    }

# GET API to fetch all call entries
@router.get("/call_planning/")
async def get_call_entries():
    calls_collection = get_collection("call_planning")
    call_entries = list(calls_collection.find())
    
    if not call_entries:
        raise HTTPException(status_code=404, detail="No call entries found.")
    
    # Serialize the data correctly
    return [
        {
            "_id": str(entry["_id"]),
            "lead_id": entry["lead_id"],
            "frequency": entry.get("frequency", None),
            "last_called": entry.get("last_called", None)
        }
        for entry in call_entries
    ]


@router.get("/call_plannings/")
async def get_call_entries():
    calls_collection = get_collection("call_planning")
    call_entries = calls_collection.find()
    return serialize_documents(call_entries)

@router.put("/{lead_id}")
async def update_call_frequency(lead_id: str, frequency: int):
    collection = get_collection("call_frequency")
    result = collection.update_one({"lead_id": lead_id}, {"$set": {"frequency": frequency}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lead not found")
    return {"message": "Call frequency updated"}
