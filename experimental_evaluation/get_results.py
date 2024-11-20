import pandas as pd
import os
console_width = os.get_terminal_size().columns

df = pd.read_csv("./experimental_evaluation/experimental_results/runs_test.csv")
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