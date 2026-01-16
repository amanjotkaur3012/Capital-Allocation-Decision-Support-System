import numpy as np
import numpy_financial as npf

def run_capital_rationing(df, budget):
    """
    Implements the Profitability Index (PI) rule for capital rationing.
    This demonstrates financial discipline over blind optimization.
    """
    # PI = (NPV + Investment) / Investment
    df['PI'] = (df['NPV'] + df['Investment']) / df['Investment']
    df = df.sort_values(by='PI', ascending=False)
    
    df['Status'] = '🔴 Defer'
    current_budget = 0
    for i in range(len(df)):
        if current_budget + df.iloc[i]['Investment'] <= budget:
            df.at[df.index[i], 'Status'] = '🟢 Fund'
            current_budget += df.iloc[i]['Investment']
            
    return df, current_budget
