from collections import defaultdict
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

API_KEY = "ak_ygzhqjyccg40pqf0wgt3qq2j"
EMAIL = "22f3001101@ds.study.iitm.ac.in"

app = FastAPI()

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: List[Event]


@app.post("/analytics")
def analytics(
    request: AnalyticsRequest,
    x_api_key: str = Header(None, alias="X-API-Key"),
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    events = request.events

    total_events = len(events)
    unique_users = len(set(e.user for e in events))

    revenue = 0.0
    user_totals = defaultdict(float)

    for e in events:
        if e.amount > 0:
            revenue += e.amount
            user_totals[e.user] += e.amount

    top_user = max(user_totals, key=user_totals.get) if user_totals else ""

    return {
        "email": EMAIL,
        "total_events": total_events,
        "unique_users": unique_users,
        "revenue": revenue,
        "top_user": top_user,
    }
