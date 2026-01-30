def simple_router(question: str):
    q = question.lower()
    if "why" in q and "revenue" in q:
        return {
            "metric": "total_revenue",
            "dimension": "time",
            "period": "latest",
            "comparison": "previous_period",
            "why": True
        }
    if "country" in q:
        return {
            "metric": "total_revenue",
            "dimension": "country",
            "period": "all",
            "comparison": "none",
            "why": False
        }
    return {"metric":"total_revenue","dimension":"time","period":"all","comparison":"none","why":False}

if __name__ == "__main__":
    print(simple_router("Why did revenue drop?"))
