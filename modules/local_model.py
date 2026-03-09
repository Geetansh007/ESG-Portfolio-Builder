try:
    from transformers import pipeline
    _TRANSFORMERS_AVAILABLE = True
except Exception:
    _TRANSFORMERS_AVAILABLE = False


class LocalModel:
    def __init__(self, model_name="gpt2"):
        self.model_name = model_name
        self.pipe = None
        if _TRANSFORMERS_AVAILABLE:
            try:
                # load a text-generation pipeline; user can set env to use a local HF model
                self.pipe = pipeline("text-generation", model=model_name)
            except Exception:
                self.pipe = None

    def generate(self, prompt, temperature=0.7, max_tokens=250):
        if self.pipe:
            try:
                out = self.pipe(prompt, do_sample=True, temperature=temperature, max_new_tokens=max_tokens, top_k=50)
                return out[0]["generated_text"]
            except Exception:
                pass

        return self._template_generate(prompt)

    def _template_generate(self, prompt):
        import re

        company = "the company"
        industry = "the sector"
        investment = "the amount"

        # try to extract amount, company, industry from prompt heuristically
        m_comp = re.search(r'in\s+([A-Za-z0-9 &\.-]+)\s*(?:in\s+([A-Za-z &\.-]+))?', prompt, re.IGNORECASE)
        if m_comp:
            company = m_comp.group(1).strip()
            if m_comp.lastindex >= 2 and m_comp.group(2):
                industry = m_comp.group(2).strip()

        m_amount = re.search(r'([₹Rs$]?\s?[0-9,\.KMkm]+)', prompt)
        if m_amount:
            investment = m_amount.group(1).strip()

        return (
            f"Investing {investment} in {company} strengthens the {industry} sector by encouraging"
            " responsible practices. This investment can increase market confidence, enable sustainable"
            " expansion, and create ripple effects where competitors adopt greener and more ethical"
            " practices, benefiting the environment and society while delivering long-term value for investors."
        )
