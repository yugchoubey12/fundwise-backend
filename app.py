from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# -------------------- CORS --------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://fundwise-frontend-omega.vercel.app",
        "http://localhost:5500",
        "http://127.0.0.1:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- Load Data --------------------
df = pd.read_excel("data/mf_cleaned.xlsx")

# -------------------- Input Schema --------------------
class UserInput(BaseModel):
    sip: int
    years: int
    goal: str

# -------------------- Risk Inference --------------------
def infer_risk_profile(sip, years, goal):
    if years >= 10 and sip >= 5000:
        return "High Risk"
    elif years >= 5:
        return "Medium Risk"
    else:
        return "Low Risk"

# -------------------- Asset Allocation --------------------
def get_allocation(risk):
    if risk == "High Risk":
        return {"Equity": 80, "Debt": 10, "Hybrid": 10}
    if risk == "Medium Risk":
        return {"Equity": 60, "Debt": 25, "Hybrid": 15}
    return {"Equity": 30, "Debt": 60, "Hybrid": 10}

# -------------------- Metric Selection --------------------
def get_metric(years):
    if years >= 7:
        return "returns_5yr"
    elif years >= 3:
        return "returns_3yr"
    return "returns_1yr"

# -------------------- Fund Selection --------------------
def pick_funds(category, metric, limit):
    filtered = df[df["category"].str.contains(category, case=False, na=False)]
    filtered = filtered.dropna(subset=[metric])
    return (
        filtered.sort_values(by=metric, ascending=False)
        .head(limit)[
            ["scheme_name", "category", "sub_category", metric]
        ]
        .to_dict(orient="records")
    )

# -------------------- API --------------------
@app.post("/recommend-funds")
def recommend_funds(user: UserInput):
    risk = infer_risk_profile(user.sip, user.years, user.goal)
    allocation = get_allocation(risk)
    metric = get_metric(user.years)

    recommendations = {
        "Equity": pick_funds("Equity", metric, 3),
        "Debt": pick_funds("Debt", metric, 1),
        "Hybrid": pick_funds("Hybrid", metric, 1),
    }

    return {
        "risk_profile": risk,
        "investment_horizon": f"{user.years} years",
        "metric_used": metric,
        "allocation": allocation,
        "recommended_funds": recommendations
    }

