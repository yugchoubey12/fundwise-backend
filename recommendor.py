import pandas as pd

DATA_PATH = "data/mf_cleaned.xlsx"

def load_fund_data():
    return pd.read_excel(DATA_PATH)

def get_return_column(years: int):
    if years <= 2:
        return "returns_1yr"
    elif years <= 4:
        return "returns_3yr"
    else:
        return "returns_5yr"

def category_by_risk(risk: str):
    if risk == "low":
        return ["Debt", "Hybrid"]
    elif risk == "medium":
        return ["Hybrid", "Index"]
    else:
        return ["Equity", "Index"]

def recommend_top_funds(risk: str, years: int, top_n: int = 5):
    df = load_fund_data()

    return_col = get_return_column(years)
    categories = category_by_risk(risk)

    df = df[df["category"].isin(categories)]
    df = df[df["rating"] >= 3]

    df = df.sort_values(by=return_col, ascending=False)

    return df[[
        "scheme_name",
        "category",
        "sub_category",
        "rating",
        return_col
    ]].head(top_n)
