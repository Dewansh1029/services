from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pymongo import MongoClient
from services.database import db

router = APIRouter()

@router.get("/show")
async def performance_tracking():
    try:
        leads = list(db["leads"].find({}))
        interactions = list(db["interactions"].find({}))

        # Performance result list
        performance_data = []

        for lead in leads:
            lead_id = str(lead["_id"])
            lead_interactions = [i for i in interactions if str(i["lead_id"]) == lead_id]

            # Calculate metrics
            total_interactions = len(lead_interactions)
            total_orders = len([i for i in lead_interactions if i["type"] == "order"])
            performance_score = total_orders * 10 + total_interactions * 5

            # Determine performance status
            if performance_score < 50:
                status = "underperforming"
            elif performance_score < 80:
                status = "average"
            else:
                status = "well-performing"

            # Append performance data
            performance_data.append({
                "lead_id": lead_id,
                "name": lead["name"],
                "performance_score": performance_score,
                "status": status,
                "total_interactions": total_interactions,
                "total_orders": total_orders
            })

        return performance_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
