import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
from modules.impact_engine import generate_impact_explanation
from modules.report_generator import generate_report
from modules.esg_scorer import calculate_esg_score
from modules.market_simulator import simulate_market_influence
import pandas as pd
import os

class ESG_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ESG Impact Generator")
        self.root.geometry("800x700")

        # Load data
        self.load_data()

        # Create widgets
        self.company_label = tk.Label(root, text="Company Name:")
        self.company_label.pack(pady=5)
        self.company_combo = ttk.Combobox(root, values=self.companies, width=57)
        self.company_combo.pack(pady=5)

        self.industry_label = tk.Label(root, text="Industry:")
        self.industry_label.pack(pady=5)
        self.industry_combo = ttk.Combobox(root, values=self.industries, width=57)
        self.industry_combo.pack(pady=5)

        self.preference_label = tk.Label(root, text="ESG Preference:")
        self.preference_label.pack(pady=5)
        self.preference_combo = ttk.Combobox(root, values=["Balanced", "Environmental", "Social", "Governance"], width=57)
        self.preference_combo.current(0)  # Default to Balanced
        self.preference_combo.pack(pady=5)

        self.investment_label = tk.Label(root, text="Investment Amount (INR):")
        self.investment_label.pack(pady=5)
        self.investment_spin = tk.Spinbox(root, from_=1000, to=100000000, width=56)
        self.investment_spin.pack(pady=5)

        self.analyze_button = tk.Button(root, text="Run Full ESG Analysis", command=self.run_full_analysis)
        self.analyze_button.pack(pady=10)

        self.report_button = tk.Button(root, text="Generate PDF Report", command=self.generate_report_pdf)
        self.report_button.pack(pady=10)

        self.output_label = tk.Label(root, text="Analysis Results:")
        self.output_label.pack(pady=10)

        self.text_output = scrolledtext.ScrolledText(root, height=25, width=90)
        self.text_output.pack(pady=10)

        self.analysis_data = {}

    def load_data(self):
        try:
            self.df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'sample_esg_data.csv'))
            self.companies = self.df['Company'].tolist()
            self.industries = self.df['Industry'].unique().tolist()
        except Exception as e:
            messagebox.showerror("Data Error", f"Failed to load data: {str(e)}")
            self.df = pd.DataFrame()
            self.companies = []
            self.industries = []

    def run_full_analysis(self):
        company = self.company_combo.get().strip()
        industry = self.industry_combo.get().strip()
        preference = self.preference_combo.get().strip()
        investment_str = self.investment_spin.get().strip()

        if not company or not industry or not investment_str:
            messagebox.showwarning("Input Error", "Please select company, industry, preference, and enter investment amount.")
            return

        try:
            investment = float(investment_str)
            if investment < 1000 or investment > 100000000:
                messagebox.showerror("Input Error", "Investment amount must be between 1,000 and 100,000,000 INR.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Investment amount must be a number.")
            return

        try:
            # Get company data
            company_data = self.df[self.df['Company'] == company].iloc[0]

            # Calculate ESG score
            esg_score = calculate_esg_score(company_data, preference)

            # Generate impact explanation
            impact_text = generate_impact_explanation(company, industry, investment)

            # Simulate market influence
            market_sim = simulate_market_influence(investment)
            market_text = f"Projected Industry Growth: {market_sim['Projected Industry Growth (%)']}%\nCompetitor Adoption Increase: {market_sim['Competitor Adoption Increase (%)']}%"

            # Build simple portfolio
            portfolio = pd.DataFrame({
                'Company': [company],
                'Industry': [industry],
                'E_score': [company_data['E_score']],
                'S_score': [company_data['S_score']],
                'G_score': [company_data['G_score']],
                'ESG_score': [esg_score],
                'Financial_score': [company_data['Financial_score']],
                'Investment_Amount': [investment]
            })

            # Store data for report
            self.analysis_data = {
                'company': company,
                'industry': industry,
                'preference': preference,
                'investment': investment,
                'company_data': company_data,
                'esg_score': esg_score,
                'impact_text': impact_text,
                'market_text': market_text,
                'portfolio': portfolio
            }

            # Display results
            result_text = f"""
COMPANY ANALYSIS REPORT
=======================

Company: {company}
Industry: {industry}
ESG Preference: {preference}

ESG SCORES:
-----------
Environmental Score: {company_data['E_score']}/100
Social Score: {company_data['S_score']}/100
Governance Score: {company_data['G_score']}/100
Financial Score: {company_data['Financial_score']}/100

Calculated ESG Score ({preference}): {esg_score:.2f}/100

INVESTMENT DETAILS:
-------------------
Investment Amount: ₹{investment:,.0f}

MARKET SIMULATION:
------------------
{market_text}

IMPACT EXPLANATION:
-------------------
{impact_text}
"""
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, result_text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")

    def generate_report_pdf(self):
        if not self.analysis_data:
            messagebox.showwarning("No Analysis", "Please run the full ESG analysis first.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if filename:
            try:
                # Create enhanced report content
                report_content = f"""
COMPANY ESG ANALYSIS REPORT

Company: {self.analysis_data['company']}
Industry: {self.analysis_data['industry']}
ESG Preference: {self.analysis_data['preference']}
Investment: ₹{self.analysis_data['investment']:,.0f}

ESG Scores:
- Environmental: {self.analysis_data['company_data']['E_score']}/100
- Social: {self.analysis_data['company_data']['S_score']}/100
- Governance: {self.analysis_data['company_data']['G_score']}/100
- Financial: {self.analysis_data['company_data']['Financial_score']}/100

Calculated ESG Score: {self.analysis_data['esg_score']:.2f}/100

Market Simulation:
{self.analysis_data['market_text']}

Impact Analysis:
{self.analysis_data['impact_text']}
"""

                generate_report(filename, self.analysis_data['portfolio'], report_content)
                messagebox.showinfo("Success", f"Complete ESG analysis report saved as {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ESG_GUI(root)
    root.mainloop()