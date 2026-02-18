import streamlit as st
import plotly.express as px

from modules.data_loader import load_data
from modules.esg_scorer import calculate_esg_score
from modules.portfolio_optimizer import build_portfolio
from modules.impact_engine import generate_impact_explanation
from modules.market_simulator import simulate_market_influence
from modules.report_generator import generate_report

st.title("🌍 InsightAgent ESG – Impact Driven Investing")

investment_amount = st.number_input("Enter Investment Amount", min_value=1000, value=100000)
preference = st.selectbox(
    "Select ESG Preference",
    ["Balanced", "Environmental", "Social", "Governance"]
)

if st.button("Generate Portfolio"):

    df = load_data()

    df["ESG_score"] = df.apply(
        lambda row: calculate_esg_score(row, preference),
        axis=1
    )

    df["final_score"] = 0.6 * df["ESG_score"] + 0.4 * df["Financial_score"]

    portfolio = build_portfolio(df, investment_amount)

    st.subheader("📊 Recommended Portfolio")
    st.dataframe(portfolio)

    fig = px.pie(
        portfolio,
        values="Investment_Amount",
        names="Company",
        title="Portfolio Allocation"
    )

    st.plotly_chart(fig)

    st.subheader("🌎 Market Influence Simulation")
    simulation = simulate_market_influence(investment_amount)
    st.write(simulation)

    selected = portfolio.iloc[0]
    impact_text = generate_impact_explanation(
        selected["Company"],
        selected["Industry"],
        selected["Investment_Amount"]
    )

    st.subheader("💡 Impact Explanation")
    st.write(impact_text)

    generate_report("impact_report.pdf", portfolio, impact_text)

    with open("impact_report.pdf", "rb") as f:
        st.download_button("Download ESG Report", f, "impact_report.pdf")
