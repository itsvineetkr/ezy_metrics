import pandas as pd

df = pd.read_csv("static/dummy_data/lead_data.csv")

print(df.value_counts("Lead_Stage"))
