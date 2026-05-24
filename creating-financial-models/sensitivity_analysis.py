"""
Sensitivity analysis module for financial models.
Tests impact of variable changes on key outputs.
"""

from collections.abc import Callable
from typing import Any
import numpy as np
import pandas as pd


class SensitivityAnalyzer:
    """Perform sensitivity analysis on financial models."""

    def __init__(self, base_model: Any):
        """Initialize sensitivity analyzer."""
        self.base_model = base_model
        self.base_output = None

    def one_way_sensitivity(
        self,
        variable_name: str,
        base_value: float,
        range_pct: float,
        steps: int,
        output_func: Callable,
        model_update_func: Callable,
    ) -> pd.DataFrame:
        """Perform one-way sensitivity analysis."""
        test_values = np.linspace(base_value * (1 - range_pct), base_value * (1 + range_pct), steps)
        results = []
        for value in test_values:
            model_update_func(value)
            output = output_func()
            results.append({"variable": variable_name, "value": value, "output": output})
        model_update_func(base_value)
        return pd.DataFrame(results)

    def scenario_analysis(
        self,
        scenarios: dict[str, dict[str, float]],
        variable_updates: dict[str, Callable],
        output_func: Callable,
    ) -> pd.DataFrame:
        """Analyze multiple scenarios."""
        results = []
        for name, vars in scenarios.items():
            for var_name, val in vars.items():
                if var_name in variable_updates: variable_updates[var_name](val)
            results.append({"scenario": name, "output": output_func(), **vars})
        return pd.DataFrame(results)

if __name__ == "__main__":
    print("Sensitivity module ready.")
