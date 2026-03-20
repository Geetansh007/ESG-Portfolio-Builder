import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from modules.report_generator import generate_report
from modules.esg_scorer import calculate_esg_score, get_industry_averages, calculate_past_returns
from modules.market_simulator import simulate_market_influence
from modules.portfolio_optimizer import build_portfolio
from modules.data_loader import load_data
import pandas as pd

class ModernESGGUI:
    def __init__(self, main_root):
        self.root = main_root
        self.root.title("🌍 ESG Investment Advisor")
        self.root.geometry("900x650")
        self.root.configure(bg='#f8fafc')
        self.root.resizable(True, True)

        # Modern color palette inspired by modern web design
        self.colors = {
            'primary': '#6366f1',        # Indigo
            'primary_dark': '#4f46e5',   # Darker indigo
            'primary_light': '#a5b4fc',  # Light indigo
            'secondary': '#ec4899',      # Pink
            'success': '#10b981',        # Emerald
            'warning': '#f59e0b',        # Amber
            'error': '#ef4444',          # Red
            'background': '#f8fafc',     # Very light gray
            'surface': '#ffffff',        # White
            'surface_hover': '#f1f5f9',  # Light blue-gray
            'text_primary': '#1e293b',   # Dark slate
            'text_secondary': '#64748b', # Medium gray
            'text_muted': '#94a3b8',     # Light gray
            'border': '#e2e8f0',         # Light border
            'shadow': '#cbd5e1'          # Shadow color
        }

        # Attribute initializations for widgets
        self.preference_var = None
        self.investment_spin = None
        self.analyze_btn = None
        self.holdings_frame = None
        self.holdings_entries = None
        self.div_preference_var = None
        self.div_analyze_btn = None

        # Load data
        self.load_data()

        # Setup modern styles
        self.setup_modern_styles()

        # Create main layout
        self.create_main_layout()

        self.analysis_data = {}

    def setup_modern_styles(self):
        """Setup modern web-inspired styles"""
        style = ttk.Style()

        # Configure modern button styles
        style.configure('Modern.TButton',
                       font=('Inter', 12, 'bold'),
                       background=self.colors['primary'],
                       foreground=self.colors['surface'],
                       borderwidth=0,
                       relief='flat',
                       padding=(24, 12))

        style.map('Modern.TButton',
                 background=[('active', self.colors['primary_dark']),
                           ('pressed', self.colors['primary_dark'])])

        # Card style
        style.configure('Card.TFrame',
                       background=self.colors['surface'],
                       borderwidth=0,
                       relief='flat')

        # Label styles
        style.configure('Hero.TLabel',
                       font=('Inter', 32, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['background'])

        style.configure('H1.TLabel',
                       font=('Inter', 24, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['surface'])

        style.configure('H2.TLabel',
                       font=('Inter', 20, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['surface'])

        style.configure('H3.TLabel',
                       font=('Inter', 16, 'bold'),
                       foreground=self.colors['text_primary'],
                       background=self.colors['surface'])

        style.configure('Body.TLabel',
                       font=('Inter', 14),
                       foreground=self.colors['text_secondary'],
                       background=self.colors['surface'])

        style.configure('Caption.TLabel',
                       font=('Inter', 12),
                       foreground=self.colors['text_muted'],
                       background=self.colors['surface'])

    def create_main_layout(self):
        """Modern layout with clear, scrollable pages and separated results"""
        # Hero section
        hero_frame = tk.Frame(self.root, bg=self.colors['primary'], height=120)
        hero_frame.pack(fill='x', side='top')
        hero_frame.pack_propagate(False)

        hero_content = tk.Frame(hero_frame, bg=self.colors['primary'])
        hero_content.pack(expand=True)

        hero_title = tk.Label(hero_content, text="🌍 ESG Investment Advisor",
                             font=('Inter', 28, 'bold'), fg=self.colors['surface'],
                             bg=self.colors['primary'])
        hero_title.pack(pady=(20, 5))

        hero_subtitle = tk.Label(hero_content, text="Make informed investment decisions with ESG intelligence",
                               font=('Inter', 14), fg=self.colors['primary_light'],
                               bg=self.colors['primary'])
        hero_subtitle.pack(pady=(0, 20))

        # Main content area with tabs
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill='both', expand=True, padx=32, pady=16)

        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill='both', expand=True)

        # --- New Investment Tab ---
        new_inv_tab = tk.Frame(notebook, bg=self.colors['background'])
        notebook.add(new_inv_tab, text="💰 New Investment")

        new_inv_canvas = tk.Canvas(new_inv_tab, bg=self.colors['background'], highlightthickness=0)
        new_inv_canvas.pack(side='left', fill='both', expand=True)
        new_inv_scroll = tk.Scrollbar(new_inv_tab, orient='vertical', command=new_inv_canvas.yview)
        new_inv_scroll.pack(side='right', fill='y')
        new_inv_canvas.configure(yscrollcommand=new_inv_scroll.set)

        self.new_inv_content = tk.Frame(new_inv_canvas, bg=self.colors['background'])
        new_inv_content_id = new_inv_canvas.create_window((0, 0), window=self.new_inv_content, anchor='nw')

        def _on_new_inv_configure(event):
            new_inv_canvas.configure(scrollregion=new_inv_canvas.bbox('all'))
        self.new_inv_content.bind('<Configure>', _on_new_inv_configure)

        def _on_new_inv_canvas_configure(event):
            new_inv_canvas.itemconfig(new_inv_content_id, width=event.width)
        new_inv_canvas.bind('<Configure>', _on_new_inv_canvas_configure)

        # --- Portfolio Diversification Tab ---
        div_tab = tk.Frame(notebook, bg=self.colors['background'])
        notebook.add(div_tab, text="📊 Portfolio Diversification")

        div_canvas = tk.Canvas(div_tab, bg=self.colors['background'], highlightthickness=0)
        div_canvas.pack(side='left', fill='both', expand=True)
        div_scroll = tk.Scrollbar(div_tab, orient='vertical', command=div_canvas.yview)
        div_scroll.pack(side='right', fill='y')
        div_canvas.configure(yscrollcommand=div_scroll.set)

        self.div_content = tk.Frame(div_canvas, bg=self.colors['background'])
        div_content_id = div_canvas.create_window((0, 0), window=self.div_content, anchor='nw')

        def _on_div_configure(event):
            div_canvas.configure(scrollregion=div_canvas.bbox('all'))
        self.div_content.bind('<Configure>', _on_div_configure)

        def _on_div_canvas_configure(event):
            div_canvas.itemconfig(div_content_id, width=event.width)
        div_canvas.bind('<Configure>', _on_div_canvas_configure)

        # Results area (now inside each tab's scrollable content)
        self.new_inv_results_frame = tk.Frame(self.new_inv_content, bg=self.colors['background'])
        self.new_inv_results_frame.pack(fill='x', padx=0, pady=(24, 0))
        self.div_results_frame = tk.Frame(self.div_content, bg=self.colors['background'])
        self.div_results_frame.pack(fill='x', padx=0, pady=(24, 0))

        # Populate input areas (clear and structured)
        self.create_modern_new_investment_inputs(self.new_inv_content)
        self.create_modern_diversification_inputs(self.div_content)

    # update_main_screen and screen_var/main_content_frame are not used in the new layout


    def create_modern_new_investment_inputs(self, parent):
        """Create modern web-inspired new investment inputs (standalone section)"""
        # ESG Preference Section
        pref_section = self.create_modern_section(parent, "🎯 ESG Investment Focus",
                                                "Choose your sustainability priorities")

        pref_container = tk.Frame(pref_section, bg=self.colors['surface'])
        pref_container.pack(pady=16)

        self.preference_var = tk.StringVar(value="Balanced")

        preferences = [
            ("Balanced", "Equal focus on all ESG factors", "⚖️"),
            ("Environmental", "Prioritize climate and sustainability", "🌱"),
            ("Social", "Focus on community and workforce", "👥"),
            ("Governance", "Emphasize corporate ethics", "🏛️")
        ]

        for pref, desc, icon in preferences:
            self.create_modern_radio_option(pref_container, pref, desc, icon, self.preference_var)

        # Investment Amount Section
        amount_section = self.create_modern_section(parent, "💵 Investment Amount",
                              "Enter the amount you want to invest")

        amount_container = tk.Frame(amount_section, bg=self.colors['surface'])
        amount_container.pack(pady=16)

        # Amount input with modern styling
        amount_frame = tk.Frame(amount_container, bg=self.colors['surface'])
        amount_frame.pack()

        # Currency symbol
        currency_label = tk.Label(amount_frame, text="₹", font=('Inter', 20, 'bold'),
                                bg=self.colors['surface'], fg=self.colors['text_primary'])
        currency_label.pack(side='left', padx=(0, 8))

        # Amount input
        self.investment_spin = tk.Spinbox(amount_frame, from_=1000, to=100000000,
                                        width=20, font=('Inter', 16),
                                        bg=self.colors['surface'], fg=self.colors['text_primary'],
                                        buttonbackground=self.colors['primary'],
                                        relief='flat', borderwidth=2)
        self.investment_spin.pack(side='left', padx=(0, 8))

        # INR label
        inr_label = tk.Label(amount_frame, text="INR", font=('Inter', 14),
                           bg=self.colors['surface'], fg=self.colors['text_secondary'])
        inr_label.pack(side='left')

        # Range indicator
        range_label = tk.Label(amount_container, text="Range: ₹1,000 - ₹10,00,00,000",
                             font=('Inter', 12), bg=self.colors['surface'],
                             fg=self.colors['text_muted'])
        range_label.pack(pady=(8, 0))

        # Action Section
        action_section = self.create_modern_section(parent, "", "")

        # Submit button with modern styling
        self.analyze_btn = tk.Button(action_section, text="Submit",
                       bg=self.colors['primary'], fg=self.colors['surface'],
                       font=('Inter', 16, 'bold'), padx=40, pady=16,
                       relief='flat', borderwidth=0, cursor='hand2',
                       command=self.run_new_investment_analysis)
        self.analyze_btn.pack(pady=16)

        # Hover effect
        self.analyze_btn.bind("<Enter>", lambda e: self.analyze_btn.config(bg=self.colors['primary_dark']))
        self.analyze_btn.bind("<Leave>", lambda e: self.analyze_btn.config(bg=self.colors['primary']))

    def create_modern_radio_option(self, parent, value, description, icon, variable):
        """Create modern radio button option"""
        option_frame = tk.Frame(parent, bg=self.colors['surface'])
        option_frame.pack(fill='x', pady=8, padx=16)

        # Radio button
        radio = tk.Radiobutton(option_frame, text="", variable=variable, value=value,
                              bg=self.colors['surface'], activebackground=self.colors['surface'],
                              selectcolor=self.colors['primary'])
        radio.pack(side='left', padx=(0, 12))

        # Content
        content_frame = tk.Frame(option_frame, bg=self.colors['surface'])
        content_frame.pack(side='left', fill='x', expand=True)

        # Icon and title
        title_frame = tk.Frame(content_frame, bg=self.colors['surface'])
        title_frame.pack(anchor='w')

        icon_label = tk.Label(title_frame, text=icon, font=('Inter', 18),
                             bg=self.colors['surface'], fg=self.colors['text_primary'])
        icon_label.pack(side='left', padx=(0, 8))

        title_label = tk.Label(title_frame, text=value, font=('Inter', 16, 'bold'),
                              bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(side='left')

        # Description
        desc_label = tk.Label(content_frame, text=description, font=('Inter', 13),
                             bg=self.colors['surface'], fg=self.colors['text_secondary'])
        desc_label.pack(anchor='w', pady=(4, 0))

    def create_modern_diversification_inputs(self, parent):
        """Create modern web-inspired diversification inputs (standalone section)"""
        # Current Holdings Section
        holdings_section = self.create_modern_section(parent, "📈 Current Portfolio",
                                                    "Enter your existing investments")

        holdings_container = tk.Frame(holdings_section, bg=self.colors['surface'])
        holdings_container.pack(pady=16, fill='x')

        # Holdings header
        holdings_header = tk.Label(holdings_container, text="Your Current Investments",
                                 font=('Inter', 16, 'bold'), bg=self.colors['surface'],
                                 fg=self.colors['text_primary'])
        holdings_header.pack(pady=(0, 16))

        # Holdings input area
        self.holdings_frame = tk.Frame(holdings_container, bg=self.colors['surface'])
        self.holdings_frame.pack(pady=8, fill='x')

        self.holdings_entries = []
        self.add_modern_holding_input()

        # Add holding button
        add_btn = tk.Button(holdings_container, text="+ Add Investment",
                           bg=self.colors['primary_light'], fg=self.colors['primary'],
                           font=('Inter', 12, 'bold'), padx=16, pady=8,
                           relief='flat', borderwidth=0, cursor='hand2',
                           command=self.add_modern_holding_input)
        add_btn.pack(pady=8)

        add_btn.bind("<Enter>", lambda e: add_btn.config(bg=self.colors['primary']))
        add_btn.bind("<Leave>", lambda e: add_btn.config(bg=self.colors['primary_light']))

        # ESG Focus Section
        focus_section = self.create_modern_section(parent, "🎯 Diversification Strategy",
                             "Choose your ESG priorities for recommendations")

        focus_container = tk.Frame(focus_section, bg=self.colors['surface'])
        focus_container.pack(pady=16)

        self.div_preference_var = tk.StringVar(value="Balanced")

        focus_options = [
            ("Balanced", "Balance all ESG factors", "⚖️"),
            ("Environmental", "Focus on green investments", "🌱"),
            ("Social", "Prioritize social impact", "👥"),
            ("Governance", "Emphasize ethical governance", "🏛️")
        ]

        for pref, desc, icon in focus_options:
            self.create_modern_radio_option(focus_container, pref, desc, icon, self.div_preference_var)

        # Action Section
        action_section = self.create_modern_section(parent, "", "")

        self.div_analyze_btn = tk.Button(action_section, text="Submit",
                           bg=self.colors['primary'], fg=self.colors['surface'],
                           font=('Inter', 16, 'bold'), padx=40, pady=16,
                           relief='flat', borderwidth=0, cursor='hand2',
                           command=self.run_diversification_analysis)
        self.div_analyze_btn.pack(pady=16)

        self.div_analyze_btn.bind("<Enter>", lambda e: self.div_analyze_btn.config(bg=self.colors['primary_dark']))
        self.div_analyze_btn.bind("<Leave>", lambda e: self.div_analyze_btn.config(bg=self.colors['primary']))

    def create_modern_section(self, parent, title, subtitle):
        """Create modern section with title and subtitle"""
        section = tk.Frame(parent, bg=self.colors['background'])
        section.pack(fill='x', pady=(0, 24))

        if title:
            title_label = tk.Label(section, text=title, font=('Inter', 20, 'bold'),
                                 bg=self.colors['background'], fg=self.colors['text_primary'])
            title_label.pack(pady=(0, 4))

        if subtitle:
            subtitle_label = tk.Label(section, text=subtitle, font=('Inter', 14),
                                    bg=self.colors['background'], fg=self.colors['text_secondary'])
            subtitle_label.pack(pady=(0, 16))

        # Section content container
        content = tk.Frame(section, bg=self.colors['surface'], padx=24, pady=24,
                          relief='raised', borderwidth=0)
        content.pack(fill='x')

        return content

    def add_modern_holding_input(self):
        """Add modern styled holding input"""
        if len(self.holdings_entries) >= 5:
            return

        # Input container with modern styling
        input_container = tk.Frame(self.holdings_frame, bg=self.colors['surface_hover'],
                                 padx=16, pady=12, relief='flat', borderwidth=1)
        input_container.pack(fill='x', pady=4)

        # Company selection
        company_frame = tk.Frame(input_container, bg=self.colors['surface_hover'])
        company_frame.pack(side='left', fill='x', expand=True)

        company_label = tk.Label(company_frame, text="Company", font=('Inter', 12, 'bold'),
                               bg=self.colors['surface_hover'], fg=self.colors['text_primary'])
        company_label.pack(anchor='w')

        company_combo = ttk.Combobox(company_frame, values=self.companies, width=25,
                                   font=('Inter', 11))
        company_combo.pack(fill='x', pady=(4, 0))

        # Amount input
        amount_frame = tk.Frame(input_container, bg=self.colors['surface_hover'])
        amount_frame.pack(side='left', padx=(16, 0))

        amount_label = tk.Label(amount_frame, text="Amount (₹)", font=('Inter', 12, 'bold'),
                              bg=self.colors['surface_hover'], fg=self.colors['text_primary'])
        amount_label.pack(anchor='w')

        amount_entry = tk.Entry(amount_frame, width=15, font=('Inter', 11),
                              bg=self.colors['surface'], fg=self.colors['text_primary'],
                              relief='flat', borderwidth=1)
        amount_entry.pack(pady=(4, 0))

        # Remove button (if not first)
        if len(self.holdings_entries) > 0:
            remove_btn = tk.Button(input_container, text="✕",
                                 bg=self.colors['error'], fg=self.colors['surface'],
                                 font=('Inter', 10, 'bold'), padx=8, pady=4,
                                 relief='flat', borderwidth=0, cursor='hand2',
                                 command=lambda: self.remove_modern_holding(input_container))
            remove_btn.pack(side='right', padx=(8, 0))

            remove_btn.bind("<Enter>", lambda e: remove_btn.config(bg='#dc2626'))
            remove_btn.bind("<Leave>", lambda e: remove_btn.config(bg=self.colors['error']))

        self.holdings_entries.append((company_combo, amount_entry, input_container))

    def remove_modern_holding(self, container):
        """Remove modern holding input"""
        for i, (_, _, frame) in enumerate(self.holdings_entries):
            if frame == container:
                frame.destroy()
                self.holdings_entries.pop(i)
                break

    def load_data(self):
        """Load ESG data"""
        try:
            self.df = load_data()
            self.companies = self.df['Company'].tolist()
            self.industries = self.df['Industry'].unique().tolist()
        except Exception:
            messagebox.showerror("Data Error", "Failed to load data")
            self.df = pd.DataFrame()
            self.companies = []
            self.industries = []

    def run_new_investment_analysis(self):
        """Run new investment analysis with modern UI feedback"""
        try:
            investment = float(self.investment_spin.get())
            preference = self.preference_var.get()

            if investment < 1000 or investment > 100000000:
                messagebox.showerror("Input Error", "Investment must be between ₹1,000 and ₹10,00,00,000")
                return

            # Show loading state
            self.analyze_btn.config(text="⏳ Analyzing...", state='disabled')

            # Run analysis with industry-relative ESG
            df = self.df.copy()
            industry_averages = get_industry_averages(df)
            df["ESG_score"] = df.apply(lambda row: calculate_esg_score(row, preference, industry_averages)["score"], axis=1)
            df["E_score"] = df.apply(lambda row: calculate_esg_score(row, preference, industry_averages)["E_score"], axis=1)
            df["S_score"] = df.apply(lambda row: calculate_esg_score(row, preference, industry_averages)["S_score"], axis=1)
            df["G_score"] = df.apply(lambda row: calculate_esg_score(row, preference, industry_averages)["G_score"], axis=1)
            df["final_score"] = 0.6 * df["ESG_score"] + 0.4 * df["Financial_score"]

            portfolio = build_portfolio(df, investment)
            market_sim = simulate_market_influence(investment)
            market_text = f"Projected Industry Growth: {market_sim['Projected Industry Growth (%)']}%\nCompetitor Adoption Increase: {market_sim['Competitor Adoption Increase (%)']}%"

            self.analysis_data = {
                'mode': 'new_investment',
                'investment': investment,
                'preference': preference,
                'portfolio': portfolio,
                'market_text': market_text
            }

            # Reset button
            self.analyze_btn.config(text="🚀 Generate Investment Plan", state='normal')

            self.show_modern_results()

        except ValueError:
            self.analyze_btn.config(text="🚀 Generate Investment Plan", state='normal')
            messagebox.showerror("Input Error", "Please enter a valid investment amount")
        except Exception as e:
            self.analyze_btn.config(text="🚀 Generate Investment Plan", state='normal')
            print(f"[ERROR] New Investment Analysis failed: {e}")
            import traceback; traceback.print_exc()
            messagebox.showerror("Error", f"Analysis failed due to an unexpected error:\n{e}")

    def run_diversification_analysis(self):
        """Run diversification analysis"""
        try:
            current_holdings = []
            total_current = 0

            for combo, entry, _ in self.holdings_entries:
                company = combo.get().strip()
                amount_str = entry.get().strip()

                if company and amount_str:
                    amount = float(amount_str)
                    current_holdings.append({'company': company, 'amount': amount})
                    total_current += amount

            if not current_holdings:
                messagebox.showerror("Input Error", "Please enter at least one current holding")
                return

            preference = self.div_preference_var.get()

            # Show loading
            self.div_analyze_btn.config(text="⏳ Analyzing...", state='disabled')

            current_analysis = self.analyze_current_portfolio(current_holdings, preference)
            recommendations = self.generate_diversification_recommendations(current_holdings, total_current, preference)

            self.analysis_data = {
                'mode': 'diversification',
                'current_holdings': current_holdings,
                'total_current': total_current,
                'preference': preference,
                'current_analysis': current_analysis,
                'recommendations': recommendations
            }

            # Reset button
            self.div_analyze_btn.config(text="🔄 Analyze & Optimize Portfolio", state='normal')

            self.show_modern_results()

        except ValueError:
            self.div_analyze_btn.config(text="🔄 Analyze & Optimize Portfolio", state='normal')
            messagebox.showerror("Input Error", "Please enter valid amounts for all holdings")
        except Exception as e:
            self.div_analyze_btn.config(text="🔄 Analyze & Optimize Portfolio", state='normal')
            print(f"[ERROR] Diversification Analysis failed: {e}")
            import traceback; traceback.print_exc()
            messagebox.showerror("Error", f"Analysis failed due to an unexpected error:\n{e}")

    def analyze_current_portfolio(self, holdings, preference):
        """Analyze current portfolio composition with industry-relative ESG"""
        analysis = {
            'companies': [],
            'total_value': 0,
            'avg_esg_score': 0,
            'sector_diversity': {},
            'risk_assessment': 'Low'
        }

        total_esg = 0
        df = self.df.copy()
        industry_averages = get_industry_averages(df)
        for holding in holdings:
            company_data = df[df['Company'] == holding['company']]
            if not company_data.empty:
                data = company_data.iloc[0]
                esg_result = calculate_esg_score(data, preference, industry_averages)
                esg_score = esg_result["score"]

                analysis['companies'].append({
                    'name': holding['company'],
                    'amount': holding['amount'],
                    'esg_score': esg_score,
                    'industry': data['Industry'],
                    'E_score': esg_result["E_score"],
                    'S_score': esg_result["S_score"],
                    'G_score': esg_result["G_score"]
                })

                analysis['total_value'] += holding['amount']
                total_esg += esg_score

                industry = data['Industry']
                if industry in analysis['sector_diversity']:
                    analysis['sector_diversity'][industry] += holding['amount']
                else:
                    analysis['sector_diversity'][industry] = holding['amount']

        if analysis['companies']:
            analysis['avg_esg_score'] = total_esg / len(analysis['companies'])

        num_sectors = len(analysis['sector_diversity'])
        if num_sectors <= 2:
            analysis['risk_assessment'] = 'High'
        elif num_sectors <= 4:
            analysis['risk_assessment'] = 'Medium'
        else:
            analysis['risk_assessment'] = 'Low'

        return analysis

    def generate_diversification_recommendations(self, current_holdings, total_current, preference):
        """Generate diversification recommendations"""
        current_industries = set()
        for holding in current_holdings:
            company_data = self.df[self.df['Company'] == holding['company']]
            if not company_data.empty:
                current_industries.add(company_data.iloc[0]['Industry'])

        all_industries = set(self.df['Industry'].unique())
        missing_industries = all_industries - current_industries

        df = self.df.copy()
        industry_averages = get_industry_averages(df)
        df["ESG_score"] = df.apply(lambda row: calculate_esg_score(row, preference, industry_averages)["score"], axis=1)
        df["E_score"] = df.apply(lambda row: calculate_esg_score(row, preference, industry_averages)["E_score"], axis=1)
        df["S_score"] = df.apply(lambda row: calculate_esg_score(row, preference, industry_averages)["S_score"], axis=1)
        df["G_score"] = df.apply(lambda row: calculate_esg_score(row, preference, industry_averages)["G_score"], axis=1)
        from modules.portfolio_optimizer import build_portfolio
        # Use same allocation logic as main portfolio (ESG + 1Y return)
        df = build_portfolio(df, total_current)

        recommendations = []
        for industry in missing_industries:
            sector_companies = df[df['Industry'] == industry].nlargest(2, 'alloc_score')
            for _, company in sector_companies.iterrows():
                recommendations.append({
                    'company': company['Company'],
                    'industry': industry,
                    'esg_score': company['ESG_score'],
                    'suggested_allocation': min(company['Investment_Amount'], 500000)
                })

        return recommendations[:5]

    def show_modern_results(self):
        """Show modern web-inspired results inside the correct tab's scrollable area"""
        if self.analysis_data['mode'] == 'new_investment':
            results_frame = self.new_inv_results_frame
        else:
            results_frame = self.div_results_frame

        # Clear previous results
        for widget in results_frame.winfo_children():
            widget.destroy()

        results_frame.pack(fill='both', expand=True, pady=(24, 32))

        if self.analysis_data['mode'] == 'new_investment':
            self.show_modern_new_investment_results(results_frame)
        else:
            self.show_modern_diversification_results(results_frame)

        # PDF Report Section
        report_section = tk.Frame(results_frame, bg=self.colors['background'])
        report_section.pack(fill='x', pady=(32, 0))

        report_content = tk.Frame(report_section, bg=self.colors['surface'],
                                padx=24, pady=24, relief='raised', borderwidth=0)
        report_content.pack(fill='x')

        report_title = tk.Label(report_content, text="📄 Generate Professional Report",
                              font=('Inter', 18, 'bold'), bg=self.colors['surface'],
                              fg=self.colors['text_primary'])
        report_title.pack(pady=(0, 8))

        report_desc = tk.Label(report_content, text="Download a comprehensive PDF report of your analysis",
                             font=('Inter', 14), bg=self.colors['surface'],
                             fg=self.colors['text_secondary'])
        report_desc.pack(pady=(0, 16))

        report_btn = tk.Button(report_content, text="📥 Download PDF Report",
                             bg=self.colors['success'], fg=self.colors['surface'],
                             font=('Inter', 14, 'bold'), padx=32, pady=12,
                             relief='flat', borderwidth=0, cursor='hand2',
                             command=self.generate_pdf_report)
        report_btn.pack()

        report_btn.bind("<Enter>", lambda e: report_btn.config(bg='#059669'))
        report_btn.bind("<Leave>", lambda e: report_btn.config(bg=self.colors['success']))

        # Update scrollregion for the current canvas so user can scroll to the bottom
        self.root.update_idletasks()
        if self.analysis_data['mode'] == 'new_investment':
            parent_canvas = self.new_inv_content.master
        else:
            parent_canvas = self.div_content.master
        parent_canvas.configure(scrollregion=parent_canvas.bbox('all'))

    def show_modern_new_investment_results(self, results_frame):
        """Show new investment results with modern design (in results_frame)"""
        data = self.analysis_data

        # Summary Cards Row
        summary_row = tk.Frame(results_frame, bg=self.colors['background'])
        summary_row.pack(fill='x', pady=(0, 24))

        # Investment Summary Card
        self.create_modern_result_card(summary_row, "💰 Investment Summary", 0, 0, 2, [
            f"Amount: ₹{data['investment']:,.0f}",
            f"ESG Focus: {data['preference']}",
            f"Portfolio Companies: {len(data['portfolio'])}"
        ])

        # Market Impact Card
        self.create_modern_result_card(summary_row, "📈 Market Impact", 0, 1, 2, [
            data['market_text'].split('\n')[0],
            data['market_text'].split('\n')[1]
        ])

        # Portfolio Recommendations
        portfolio_section = tk.Frame(results_frame, bg=self.colors['background'])
        portfolio_section.pack(fill='x')

        port_title = tk.Label(portfolio_section, text="🎯 Recommended Portfolio",
                            font=('Inter', 20, 'bold'), bg=self.colors['background'],
                            fg=self.colors['text_primary'])
        port_title.pack(pady=(0, 16))

        # Top recommendations
        for i, (_, company) in enumerate(data['portfolio'].head(4).iterrows()):
            self.create_modern_portfolio_card(portfolio_section, company, i % 2)

    def show_modern_diversification_results(self, results_frame):
        """Show diversification results with modern design (in results_frame)"""
        data = self.analysis_data
        analysis = data['current_analysis']

        # Current Portfolio Overview
        overview_row = tk.Frame(results_frame, bg=self.colors['background'])
        overview_row.pack(fill='x', pady=(0, 24))

        self.create_modern_result_card(overview_row, "📊 Current Portfolio", 0, 0, 2, [
            f"Total Value: ₹{analysis['total_value']:,.0f}",
            f"Average ESG Score: {analysis['avg_esg_score']:.1f}/100",
            f"Risk Level: {analysis['risk_assessment']}",
            f"Sectors: {len(analysis['sector_diversity'])}"
        ])

        # Current Holdings
        holdings_section = tk.Frame(results_frame, bg=self.colors['background'])
        holdings_section.pack(fill='x', pady=(0, 24))

        holdings_title = tk.Label(holdings_section, text="📈 Your Current Holdings",
                                font=('Inter', 20, 'bold'), bg=self.colors['background'],
                                fg=self.colors['text_primary'])
        holdings_title.pack(pady=(0, 16))

        for i, company in enumerate(analysis['companies'][:4]):
            self.create_modern_holding_card(holdings_section, company, i % 2)

        # Recommendations
        if data['recommendations']:
            rec_section = tk.Frame(results_frame, bg=self.colors['background'])
            rec_section.pack(fill='x')

            rec_title = tk.Label(rec_section, text="💡 Diversification Recommendations",
                               font=('Inter', 20, 'bold'), bg=self.colors['background'],
                               fg=self.colors['text_primary'])
            rec_title.pack(pady=(0, 16))

            for i, rec in enumerate(data['recommendations'][:4]):
                self.create_modern_recommendation_card(rec_section, rec, i % 2)

    def create_modern_result_card(self, parent, title, row, col, colspan, items):
        """Create modern result card (using pack)"""
        card_container = tk.Frame(parent, bg=self.colors['shadow'], padx=2, pady=2)
        card_container.pack(fill='x', padx=8, pady=8)

        card = tk.Frame(card_container, bg=self.colors['surface'], padx=24, pady=24)
        card.pack(fill='both', expand=True)

        title_label = tk.Label(card, text=title, font=('Inter', 16, 'bold'),
                             bg=self.colors['surface'], fg=self.colors['text_primary'])
        title_label.pack(pady=(0, 16))

        for item in items:
            item_label = tk.Label(card, text=item, font=('Inter', 14),
                                bg=self.colors['surface'], fg=self.colors['text_secondary'])
            item_label.pack(anchor='w', pady=2)

        return card

    def create_modern_portfolio_card(self, parent, company_data, column):
        """Create modern portfolio recommendation card (using pack)"""
        card_container = tk.Frame(parent, bg=self.colors['shadow'], padx=2, pady=2)
        card_container.pack(fill='x', padx=8, pady=8)

        card = tk.Frame(card_container, bg=self.colors['surface'], padx=24, pady=24)
        card.pack(fill='both', expand=True)

        # Company name
        company_label = tk.Label(card, text=company_data['Company'],
                               font=('Inter', 18, 'bold'), bg=self.colors['surface'],
                               fg=self.colors['text_primary'])
        company_label.pack(pady=(0, 8))

        # Industry
        industry_label = tk.Label(card, text=company_data['Industry'],
                                font=('Inter', 12), bg=self.colors['surface'],
                                fg=self.colors['text_muted'])
        industry_label.pack(pady=(0, 16))

        # ESG Score
        esg_label = tk.Label(card, text=f"ESG Score: {company_data['ESG_score']:.1f}/100",
                           font=('Inter', 14, 'bold'), bg=self.colors['surface'],
                           fg=self.colors['primary'])
        esg_label.pack(pady=(0, 8))

        # Allocation
        alloc_label = tk.Label(card, text=f"Allocation: ₹{company_data['Investment_Amount']:,.0f}",
                             font=('Inter', 14), bg=self.colors['surface'],
                             fg=self.colors['text_secondary'])
        alloc_label.pack(pady=(0, 8))

        # Percentage
        pct_label = tk.Label(card, text=f"({company_data['Allocation_%']:.1%} of portfolio)",
                           font=('Inter', 12), bg=self.colors['surface'],
                           fg=self.colors['text_muted'])
        pct_label.pack()

        return card

    def create_modern_holding_card(self, parent, company_data, column):
        """Create modern current holding card (using pack)"""
        card_container = tk.Frame(parent, bg=self.colors['shadow'], padx=2, pady=2)
        card_container.pack(fill='x', padx=8, pady=8)

        card = tk.Frame(card_container, bg=self.colors['surface'], padx=24, pady=24)
        card.pack(fill='both', expand=True)

        company_label = tk.Label(card, text=company_data['name'],
                               font=('Inter', 16, 'bold'), bg=self.colors['surface'],
                               fg=self.colors['text_primary'])
        company_label.pack(pady=(0, 4))

        amount_label = tk.Label(card, text=f"₹{company_data['amount']:,.0f}",
                              font=('Inter', 14), bg=self.colors['surface'],
                              fg=self.colors['text_secondary'])
        amount_label.pack(pady=(0, 8))

        esg_label = tk.Label(card, text=f"ESG Score: {company_data['esg_score']:.1f}",
                           font=('Inter', 13), bg=self.colors['surface'],
                           fg=self.colors['primary'])
        esg_label.pack()

        return card

    def create_modern_recommendation_card(self, parent, rec_data, column):
        """Create modern recommendation card (using pack)"""
        card_container = tk.Frame(parent, bg=self.colors['shadow'], padx=2, pady=2)
        card_container.pack(fill='x', padx=8, pady=8)

        card = tk.Frame(card_container, bg=self.colors['success'], padx=24, pady=24)
        card.pack(fill='both', expand=True)

        company_label = tk.Label(card, text=rec_data['company'],
                               font=('Inter', 16, 'bold'), bg=self.colors['success'],
                               fg=self.colors['surface'])
        company_label.pack(pady=(0, 4))

        industry_label = tk.Label(card, text=rec_data['industry'],
                                font=('Inter', 12), bg=self.colors['success'],
                                fg='#dcfce7')
        industry_label.pack(pady=(0, 8))

        esg_label = tk.Label(card, text=f"ESG Score: {rec_data['esg_score']:.1f}",
                           font=('Inter', 14, 'bold'), bg=self.colors['success'],
                           fg=self.colors['surface'])
        esg_label.pack(pady=(0, 8))

        amount_label = tk.Label(card, text=f"Suggested: ₹{rec_data['suggested_allocation']:,.0f}",
                              font=('Inter', 13), bg=self.colors['success'],
                              fg=self.colors['surface'])
        amount_label.pack()

        return card

    def generate_pdf_report(self):
        """Generate PDF report"""
        if not self.analysis_data:
            messagebox.showwarning("No Data", "Please run an analysis first")
            return

        import datetime
        today = datetime.date.today().strftime("%Y-%m-%d")
        if self.analysis_data.get('mode') == 'new_investment':
            default_name = f"ESG_Investment_Report_{today}.pdf"
        else:
            default_name = f"ESG_Diversification_Report_{today}.pdf"
        filename = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=default_name
        )
        if filename:
            try:
                if self.analysis_data['mode'] == 'new_investment':
                    self.generate_new_investment_report(filename)
                else:
                    self.generate_diversification_report(filename)

                messagebox.showinfo("Success", f"Report saved as {filename}")
            except Exception as e:
                print(f"[ERROR] Report generation failed: {e}")
                import traceback; traceback.print_exc()
                messagebox.showerror("Error", f"Failed to generate report due to an unexpected error:\n{e}")

    def generate_new_investment_report(self, filename):
        """Generate new investment PDF report"""
        data = self.analysis_data

        report_content = f"""
ESG INVESTMENT PLAN REPORT

INVESTMENT DETAILS:
- Amount: ₹{data['investment']:,.0f}
- ESG Focus: {data['preference']}

MARKET ANALYSIS:
{data['market_text']}

RECOMMENDED PORTFOLIO:
"""

        for _, company in data['portfolio'].head(5).iterrows():
            report_content += f"""
• {company['Company']} ({company['Industry']})
  ESG Score: {company['ESG_score']:.1f}
  Allocation: ₹{company['Investment_Amount']:,.0f} ({company['Allocation_%']:.1%})
"""

        generate_report(filename, data['portfolio'], report_content)

    def generate_diversification_report(self, filename):
        """Generate diversification PDF report"""
        data = self.analysis_data
        analysis = data['current_analysis']

        report_content = f"""
PORTFOLIO DIVERSIFICATION REPORT

CURRENT PORTFOLIO:
- Total Value: ₹{analysis['total_value']:,.0f}
- Average ESG Score: {analysis['avg_esg_score']:.1f}
- Risk Level: {analysis['risk_assessment']}
- Sectors: {len(analysis['sector_diversity'])}

CURRENT HOLDINGS:
"""

        for company in analysis['companies']:
            report_content += f"""
• {company['name']}: ₹{company['amount']:,.0f} (ESG: {company['esg_score']:.1f})
"""

        report_content += "\n\nRECOMMENDATIONS:\n"
        for rec in data['recommendations']:
            report_content += f"""
• {rec['company']} ({rec['industry']})
  ESG Score: {rec['esg_score']:.1f}
  Suggested Addition: ₹{rec['suggested_allocation']:,.0f}
"""

        portfolio_df = pd.DataFrame({
            'Company': [c['name'] for c in analysis['companies']],
            'Investment_Amount': [c['amount'] for c in analysis['companies']]
        })

        generate_report(filename, portfolio_df, report_content)

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernESGGUI(root)
    root.mainloop()