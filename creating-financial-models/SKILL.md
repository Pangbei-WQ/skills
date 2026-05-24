---
name: creating-financial-models
description: This skill provides an advanced financial modeling suite with DCF analysis, sensitivity testing, Monte Carlo simulations, and scenario planning for investment decisions.
---

# Financial Modeling Skill

A comprehensive financial modeling toolkit for investment analysis, valuation, and risk assessment using industry-standard methodologies.

## Capabilities

### 1. Discounted Cash Flow (DCF) Analysis
- Build complete DCF models with multiple growth scenarios
- Calculate terminal values using perpetuity growth and exit multiple methods
- Determine Weighted Average Cost of Capital (WACC)

### 2. Sensitivity Analysis
- Test key assumptions impact on valuation
- Create 2-way sensitivity tables
- Generate data for tornado charts to identify key value drivers

### 3. Scenario Planning
- Build best/base/worst case scenarios
- Model different economic environments
- Compare outcome probabilities and expected values

## How to Use

1. **Input Historicals**: Provide 3-5 years of historical revenue, EBITDA, Capex, and NWC.
2. **Set Assumptions**: Define growth rates, margins, tax rates, and terminal growth.
3. **WACC Calculation**: Provide beta, risk-free rate, and market premium.
4. **Run Analysis**: Execute DCF, sensitivity, or scenario modules.

## Scripts Included

- `dcf_model.py`: Complete DCF valuation engine.
- `sensitivity_analysis.py`: Sensitivity testing and scenario planning framework.

## Best Practices

1. Always validate balance sheet and cash flow consistency.
2. Use sensitivity analysis to identify the most critical "value drivers".
3. Document all key assumptions clearly.
4. Triangulate valuation using multiple methods if possible.
