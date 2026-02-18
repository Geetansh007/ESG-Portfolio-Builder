def build_portfolio(df, investment_amount):
    df = df.sort_values("final_score", ascending=False)
    top_companies = df.head(5).copy()

    total_score = top_companies["final_score"].sum()

    top_companies["Allocation_%"] = (
        top_companies["final_score"] / total_score
    )

    top_companies["Investment_Amount"] = (
        top_companies["Allocation_%"] * investment_amount
    )

    return top_companies
