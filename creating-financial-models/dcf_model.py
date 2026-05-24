"""
Discounted Cash Flow (DCF) valuation model.
Implements enterprise valuation using free cash flow projections.
"""

from typing import Any
import numpy as np


class DCFModel:
    """Build and calculate DCF valuation models."""

    def __init__(self, company_name: str = "Company"):
        """
        Initialize DCF model.

        Args:
            company_name: Name of the company being valued
        """
        self.company_name = company_name
        self.historical_financials = {}
        self.projections = {}
        self.assumptions = {}
        self.wacc_components = {}
        self.valuation_results = {}

    def set_historical_financials(
        self,
        revenue: list[float],
        ebitda: list[float],
        capex: list[float],
        nwc: list[float],
        years: list[int],
    ):
        """Set historical financial data."""
        self.historical_financials = {
            "years": years,
            "revenue": revenue,
            "ebitda": ebitda,
            "capex": capex,
            "nwc": nwc,
            "ebitda_margin": [ebitda[i] / revenue[i] for i in range(len(revenue))],
            "capex_percent": [capex[i] / revenue[i] for i in range(len(revenue))],
        }

    def set_assumptions(
        self,
        projection_years: int = 5,
        revenue_growth: list[float] = None,
        ebitda_margin: list[float] = None,
        tax_rate: float = 0.25,
        capex_percent: list[float] = None,
        nwc_percent: list[float] = None,
        terminal_growth: float = 0.03,
    ):
        """Set projection assumptions."""
        if revenue_growth is None:
            revenue_growth = [0.10] * projection_years

        if ebitda_margin is None:
            if self.historical_financials:
                avg_margin = np.mean(self.historical_financials["ebitda_margin"])
                ebitda_margin = [avg_margin] * projection_years
            else:
                ebitda_margin = [0.20] * projection_years

        if capex_percent is None:
            capex_percent = [0.05] * projection_years

        if nwc_percent is None:
            nwc_percent = [0.10] * projection_years

        self.assumptions = {
            "projection_years": projection_years,
            "revenue_growth": revenue_growth,
            "ebitda_margin": ebitda_margin,
            "tax_rate": tax_rate,
            "capex_percent": capex_percent,
            "nwc_percent": nwc_percent,
            "terminal_growth": terminal_growth,
        }

    def calculate_wacc(
        self,
        risk_free_rate: float,
        beta: float,
        market_premium: float,
        cost_of_debt: float,
        debt_to_equity: float,
        tax_rate: float | None = None,
    ) -> float:
        """Calculate Weighted Average Cost of Capital (WACC)."""
        if tax_rate is None:
            tax_rate = self.assumptions.get("tax_rate", 0.25)

        cost_of_equity = risk_free_rate + beta * market_premium
        equity_weight = 1 / (1 + debt_to_equity)
        debt_weight = debt_to_equity / (1 + debt_to_equity)
        wacc = equity_weight * cost_of_equity + debt_weight * cost_of_debt * (1 - tax_rate)

        self.wacc_components = {
            "wacc": wacc,
            "cost_of_equity": cost_of_equity,
            "equity_weight": equity_weight,
            "debt_weight": debt_weight,
        }
        return wacc

    def project_cash_flows(self) -> dict[str, list[float]]:
        """Project future cash flows based on assumptions."""
        years = self.assumptions["projection_years"]
        base_revenue = self.historical_financials["revenue"][-1] if self.historical_financials else 1000
        prev_revenue = base_revenue
        prev_nwc = base_revenue * 0.10

        projections = {
            "year": list(range(1, years + 1)),
            "revenue": [],
            "ebitda": [],
            "fcf": [],
        }

        for i in range(years):
            revenue = prev_revenue * (1 + self.assumptions["revenue_growth"][i])
            ebitda = revenue * self.assumptions["ebitda_margin"][i]
            capex = revenue * self.assumptions["capex_percent"][i]
            nwc = revenue * self.assumptions["nwc_percent"][i]
            nwc_change = nwc - prev_nwc
            
            # Simple FCF calculation for the tool
            tax = (ebitda - capex) * self.assumptions["tax_rate"]
            fcf = ebitda - tax - capex - nwc_change
            
            projections["revenue"].append(revenue)
            projections["ebitda"].append(ebitda)
            projections["fcf"].append(fcf)
            prev_revenue = revenue
            prev_nwc = nwc

        self.projections = projections
        return projections

    def calculate_enterprise_value(self) -> dict[str, Any]:
        """Discount cash flows to find enterprise value."""
        if not self.projections: self.project_cash_flows()
        wacc = self.wacc_components["wacc"]
        
        # PV of FCF
        pv_fcf = sum([fcf / (1 + wacc)**(i+1) for i, fcf in enumerate(self.projections["fcf"])])
        
        # Terminal Value (Growth method)
        final_fcf = self.projections["fcf"][-1]
        terminal_growth = self.assumptions["terminal_growth"]
        terminal_value = (final_fcf * (1 + terminal_growth)) / (wacc - terminal_growth)
        pv_terminal = terminal_value / (1 + wacc)**self.assumptions["projection_years"]
        
        enterprise_value = pv_fcf + pv_terminal
        self.valuation_results = {
            "enterprise_value": enterprise_value,
            "pv_fcf": pv_fcf,
            "pv_terminal": pv_terminal,
            "terminal_percent": (pv_terminal / enterprise_value) * 100
        }
        return self.valuation_results

    def generate_summary(self) -> str:
        """Generate text summary of valuation results."""
        if not self.valuation_results: return "Run valuation first."
        return f"DCF Valuation Summary: {self.company_name}\nEV: ${self.valuation_results['enterprise_value']:,.2f}M\nTerminal %: {self.valuation_results['terminal_percent']:.1f}%"

if __name__ == "__main__":
    model = DCFModel("TechCorp")
    model.set_historical_financials([100, 120], [20, 25], [5, 6], [10, 12], [2023, 2024])
    model.set_assumptions(projection_years=5)
    model.calculate_wacc(0.04, 1.2, 0.07, 0.05, 0.5)
    model.calculate_enterprise_value()
    print(model.generate_summary())
