import numpy as np
import numpy_financial as npf
import pandas as pd

def get_financial_metrics(investment, cash_flows, rate):
    flows = [-investment] + cash_flows
    npv = npf.npv(rate, flows)
    irr = npf.irr(flows)
    # Profitability Index (PI) - Key for Capital Rationing
    pi = (npv + investment) / investment if investment > 0 else 0
    return {"NPV": npv, "IRR": irr, "PI": pi}

def apply_capital_rationing(df, budget):
    """Sorts by Profitability Index to maximize NPV under constraint."""
    df = df.sort_values(by='PI', ascending=False).reset_index(drop=True)
    df['Decision'] = '🔴 Defer'
    cumulative_spend = 0
    
    for i in range(len(df)):
        if cumulative_spend + df.iloc[i]['Investment'] <= budget:
            df.at[i, 'Decision'] = '🟢 Fund'
            cumulative_spend += df.iloc[i]['Investment']
            
    return df, cumulative_spend
