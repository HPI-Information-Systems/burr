import pandas as pd
import os
console_width = os.get_terminal_size().columns
pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.width', None)  # Auto-adjust the width to fit the screen
pd.set_option('display.max_colwidth', None)  # Display the full column width
def format_time(seconds):
    """
    Convert seconds into m:ss,milliseconds format.
    """
    minutes = int(seconds // 60)
    seconds_remainder = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes}:{seconds_remainder:02},{milliseconds:03}"

df = pd.read_csv("./experimental_evaluation/experimental_results/runs_paperrun_0112.csv")
df['inference_time'].apply(lambda x: x/60)
df = df[df['group'] == 'real_world']
results = df.groupby(["group", "base_scenario", "scenario", "system"]).agg({
    # "m_cls_f1": ["mean"],
    # "m_rel_f1": ["mean" ],
    # "m_attr_f1": ["mean" ],
    # "n_cls_f1": ["mean"],
    # "n_rel_f1": ["mean"],
    # "n_attr_f1": ["mean"],
    "inference_time": ["mean"],
}).applymap(lambda x: round(x, 2))
results = results.reset_index()
results[("inference_time", "mean")] = results[("inference_time", "mean")].apply(format_time)


    
print(results)
print("\n\n")