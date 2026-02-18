from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_KEY,
    AZURE_DEPLOYMENT_NAME
)

def generate_impact_explanation(company, industry, investment):

    client = AzureOpenAI(
        api_key=AZURE_OPENAI_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version="2024-02-01"
    )

    prompt = f"""
    Explain in simple terms how investing {investment} in {company},
    which operates in the {industry} industry,
    can influence market demand and encourage sustainable practices.
    Focus on ESG and real-world impact.
    """

    response = client.chat.completions.create(
        model=AZURE_DEPLOYMENT_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6
    )

    return response.choices[0].message.content
