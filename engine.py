import numpy as np
import numpy_financial as npf

def calculate_capital_rationing(df, budget):
    # Calculate Profitability Index (PI) for ranking efficiency
    # PI = (NPV + Investment) / Investment
    df['PI'] = (df['NPV'] + df['Investment']) / df['Investment']
    df = df.sort_values(by='PI', ascending=False)
    
    df['Decision'] = '🔴 Defer'
    current_spend = 0
    for i in range(len(df)):
        if current_spend + df.iloc[i]['Investment'] <= budget:
            df.at[df.index[i], 'Decision'] = '🟢 Fund'
            current_spend += df.iloc[i]['Investment']
            
    return df, current_spend
