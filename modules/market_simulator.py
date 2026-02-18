def simulate_market_influence(total_investment):
    projected_industry_growth = total_investment * 0.08
    competitor_adoption_rate = min(5 + total_investment / 1000000, 20)

    return {
        "Projected Industry Growth (%)": round(projected_industry_growth, 2),
        "Competitor Adoption Increase (%)": round(competitor_adoption_rate, 2)
    }
