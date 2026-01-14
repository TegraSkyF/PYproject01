import pandas as pd
from analysis import calculate_kpis

data = {
    'date': pd.date_range(start='2023-01-01', periods=5),
    'sessions': [100, 150, 200, 120, 180],
    'revenue': [1000, 1500, 2000, 1200, 1800],
    'conversions': [10, 15, 20, 12, 18]
}
df = pd.DataFrame(data)
result = calculate_kpis(df)
print('Result:', result)
print('Sum of sessions:', sum([100, 150, 200, 120, 180]))
print('Sum of conversions:', sum([10, 15, 20, 12, 18]))
print('Conversion rate calc:', (10+15+20+12+18)/(100+150+200+120+180)*100)