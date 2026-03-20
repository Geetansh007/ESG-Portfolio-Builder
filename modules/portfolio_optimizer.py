from modules.esg_scorer import calculate_past_returns

def build_portfolio(df, investment_amount):
    # Calculate past returns for each company
    df = df.copy()
    df["Return_1Y"], df["Return_3Y"] = zip(*df.apply(calculate_past_returns, axis=1))
    # Use both ESG and 1Y return for allocation (weighted average)
    # Normalize ESG and Return_1Y to 0-1
    esg_min, esg_max = df["ESG_score"].min(), df["ESG_score"].max()
    ret_min, ret_max = df["Return_1Y"].min(), df["Return_1Y"].max()
    df["ESG_norm"] = (df["ESG_score"] - esg_min) / (esg_max - esg_min) if esg_max > esg_min else 1
    df["Return_norm"] = (df["Return_1Y"] - ret_min) / (ret_max - ret_min) if ret_max > ret_min else 1
    # Weighted: 60% ESG, 40% 1Y return
    df["alloc_score"] = 0.6 * df["ESG_norm"] + 0.4 * df["Return_norm"]
    df = df.sort_values("alloc_score", ascending=False)
    top_companies = df.head(5).copy()
    total_score = top_companies["alloc_score"].sum()
    top_companies["Allocation_%"] = top_companies["alloc_score"] / total_score if total_score > 0 else 1/5
    top_companies["Investment_Amount"] = top_companies["Allocation_%"] * investment_amount
    return top_companies
