import numpy as np
import numpy_financial as npf
import pandas as pd

def calculate_metrics(initial_investment, cash_flows, discount_rate):
    """Calculates core capital budgeting metrics."""
    # Ensure investment is negative
    flows = [initial_investment if initial_investment < 0 else -initial_investment] + cash_flows
    
    npv = npf.npv(discount_rate, flows)
    try:
        irr = npf.irr(flows)
    except:
        irr = 0
    
    # Payback Period
    cumulative_cf = np.cumsum(flows)
    payback = "N/A"
    for i, val in enumerate(cumulative_cf):
        if val >= 0:
            payback = i
            break
            
    return {
        "NPV": npv,
        "IRR": irr,
        "Payback": payback,
        "PI": (npv + abs(initial_investment)) / abs(initial_investment) if initial_investment != 0 else 0
    }

def solve_capital_rationing(projects_df, budget_limit):
    """
    Solves the Knapsack problem for capital rationing 
    prioritizing NPV within a budget constraint.
    """
    projects_df = projects_df.sort_values(by="PI", ascending=False)
    selected = []
    total_spent = 0
    
    for _, row in projects_df.iterrows():
        if total_spent + row['Investment'] <= budget_limit:
            selected.append(row['Project Name'])
            total_spent += row['Investment']
            
    return selected, total_spent
