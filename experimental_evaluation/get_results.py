import pandas as pd
import os
console_width = os.get_terminal_size().columns
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', None)  # Auto-adjust the width to fit the screen
pd.set_option('display.max_colwidth', None)  # Display the full column width

df = pd.read_csv("./experimental_evaluation/experimental_results/runs_run_2011.csv")
results = df.groupby(["group", "base_scenario", "system"]).agg({
    "m_cls_f1": ["mean", "count"],
    "m_rel_f1": ["mean", "count"],
    "m_attr_f1": ["mean", "count"],
    "n_cls_f1": ["mean", "count"],
    "n_rel_f1": ["mean", "count"],
    "n_attr_f1": ["mean", "count"],
    })
print(results)
print("\n\n")