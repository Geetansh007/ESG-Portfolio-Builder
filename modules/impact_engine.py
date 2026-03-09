from openai import OpenAI
from config import OPENAI_API_KEY, MODEL_BACKEND

# Initialize client only if key exists and backend is OpenAI
client = None
if OPENAI_API_KEY and MODEL_BACKEND == "openai":
    client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize local model if requested
local_model = None
if MODEL_BACKEND == "local":
    try:
        try:
            from modules.local_model import LocalModel
        except Exception:
            from local_model import LocalModel

        local_model = LocalModel()
    except Exception:
        local_model = None


def fallback_explanation(company, industry, investment):
    """
    Free fallback explanation (no API needed)
    """

    return f"""
Investing ₹{investment:,.0f} in {company} strengthens the {industry} sector,
especially companies that follow strong ESG practices.

This investment increases market confidence in responsible businesses,
allowing {company} to expand sustainable operations.

As more investors support ESG leaders, competitors are encouraged to adopt
similar environmental and ethical practices to remain competitive.

Over time, this creates a positive chain reaction where entire industries
move toward sustainability, benefiting society, the environment, and investors.
"""


def generate_impact_explanation(company, industry, investment):
    prompt = f"""
Explain how investing {investment} INR in {company} in {industry}
creates ESG impact and encourages sustainable market change.
"""

    # If configured to use a local model, prefer that (offline)
    if MODEL_BACKEND == "local" and local_model:
        try:
            return local_model.generate(prompt, temperature=0.7, max_tokens=250)
        except Exception:
            return fallback_explanation(company, industry, investment)

    # Try OpenAI if available
    if client:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=250
            )

            return response.choices[0].message.content

        except Exception:
            return fallback_explanation(company, industry, investment)

    # Fallback when no model is available
    return fallback_explanation(company, industry, investment)