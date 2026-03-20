import pandas as pd

def calculate_esg_score(row, preference, industry_averages=None):
    # Industry-relative scoring: compare to industry average if provided
    e, s, g = row["E_score"], row["S_score"], row["G_score"]
    if industry_averages is not None:
        ind = row["Industry"]
        e_avg = industry_averages[ind]["E_score"]
        s_avg = industry_averages[ind]["S_score"]
        g_avg = industry_averages[ind]["G_score"]
        # Score is percent above/below industry average
        e_rel = (e - e_avg) / e_avg * 100 if e_avg else 0
        s_rel = (s - s_avg) / s_avg * 100 if s_avg else 0
        g_rel = (g - g_avg) / g_avg * 100 if g_avg else 0
    else:
        e_rel = s_rel = g_rel = 0

    # Weighting by preference (can be made industry-specific)
    if preference == "Environmental":
        score = 0.6 * e + 0.2 * s + 0.2 * g
    elif preference == "Social":
        score = 0.2 * e + 0.6 * s + 0.2 * g
    elif preference == "Governance":
        score = 0.2 * e + 0.2 * s + 0.6 * g
    else:
        score = (e + s + g) / 3

    return {
        "score": score,
        "E_score": e,
        "S_score": s,
        "G_score": g,
        "E_vs_industry": e_rel,
        "S_vs_industry": s_rel,
        "G_vs_industry": g_rel
    }

def get_industry_averages(df):
    return df.groupby("Industry")[["E_score","S_score","G_score"]].mean().to_dict("index")

def calculate_past_returns(row):
    # 1Y and 3Y total return with dividends
    try:
        price_1y = float(row["Price_1Y_Ago"])
        price_3y = float(row["Price_3Y_Ago"])
        price_now = float(row["Current_Price"])
        div_1y = float(row.get("Dividends_1Y", 0))
        div_3y = float(row.get("Dividends_3Y", 0))
        ret_1y = ((price_now - price_1y + div_1y) / price_1y) * 100 if price_1y else 0
        ret_3y = ((price_now - price_3y + div_3y) / price_3y) * 100 if price_3y else 0
        return ret_1y, ret_3y
    except Exception:
        return None, None
