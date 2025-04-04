import pandas as pd
import os

# Configure display options for the console
console_width = os.get_terminal_size().columns
pd.set_option('display.max_rows', None)         # Display all rows
pd.set_option('display.max_columns', None)      # Display all columns
pd.set_option('display.width', None)            # Auto-adjust the width to fit the screen
pd.set_option('display.max_colwidth', None)       # Display the full column width

def convert_numbers(df):
    return df.applymap(lambda x: f"{x:.2f}" if isinstance(x, (int, float)) else x)

def stringify_groupby(groupby_obj):
    groupby_obj = convert_numbers(groupby_obj)
    print(groupby_obj)
    values = groupby_obj.values.flatten()
    # Convert to string and concatenate with "&"
    return " & ".join(map(str, values)) + " \\\\"

def format_time(seconds):
    """
    Convert seconds into m:ss,milliseconds format.
    """
    minutes = int(seconds // 60)
    seconds_remainder = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{minutes}:{seconds_remainder:02},{milliseconds:03}"

# Load your data
# df = pd.read_csv("./experimental_evaluation/experimental_results/runs_docker-run-8.csv")
df = pd.read_csv("./experimental_evaluation/experimental_results/runs_chatgpt_2.csv")

# Specify custom order for the "system" column
desired_order = ["d2rmapper", "rdb2onto", "ontogenix", "chatgpt"]
df["system"] = pd.Categorical(df["system"], categories=desired_order, ordered=True)

orig_data = df.copy()
metrics = {
    "m_cls_f1": ["mean"],
    "m_rel_f1": ["mean"],
    "m_attr_f1": ["mean"],
    "n_cls_f1": ["mean"],
    "n_rel_f1": ["mean"],
    "n_attr_f1": ["mean"],
    # "inference_time": ["mean"],
}

print("================ BASIC ================")
print(stringify_groupby(df[df['group'] == 'basic'].groupby(["system"]).agg(metrics)))

print("================ Attributes ================")
print(stringify_groupby(df[df['group'] == 'attributes'].groupby(["system"]).agg(metrics)))

print("================ Normalized ================")
print(stringify_groupby(df[df['group'] == 'normalized'].groupby(["system"]).agg(metrics)))
print(df[df['group'] == 'normalized'].groupby(["system", "base_scenario"]).agg(metrics))

print("================ Relationships ================")
combined_groups = ['one_to_one', 'nm_tables', 'one_to_n']
print(stringify_groupby(df[df['group'].isin(combined_groups)].groupby("system").agg(metrics)))

print("================ One to One ================")
print(stringify_groupby(df[df['group'] == 'one_to_one'].groupby(["system"]).agg(metrics)))

print("================ One to N =================")
print(stringify_groupby(df[df['group'] == 'one_to_n'].groupby(["system"]).agg(metrics)))

print("================ NM Table ================")
print(stringify_groupby(df[df['group'] == 'nm_tables'].groupby(["system"]).agg(metrics)))

print("================ Hierarchy ================")
print(stringify_groupby(df[df['group'] == 'hierarchy'].groupby(["system"]).agg(metrics)))

print("================ AVERAGE ================")
c_df = df.copy()
combined_groups = ['one_to_one', 'nm_table', 'one_to_n']
c_df['modified_group'] = df['group'].apply(lambda x: 'combined_group' if x in combined_groups else x)
print(stringify_groupby(
    c_df[c_df['modified_group'] != 'real_world']
    .groupby(["system"])
    .agg(metrics)
))

print("================ Real World ================")
print("================ Average ================")
print(stringify_groupby(df[df['group'] == 'real_world'].groupby(["system"]).agg(metrics)))
print("================ Mondial ================")
print(stringify_groupby(df[(df['base_scenario'] == 'mondial') & (df['scenario'] == 'original')].groupby(["system"]).agg(metrics)))

print("================ Mondial FK ================")
print(stringify_groupby(df[(df['base_scenario'] == 'mondial') & (df['scenario'] == 'fk')].groupby(["system"]).agg(metrics)))

print("================ RBA ================")
print(stringify_groupby(df[df['base_scenario'] == 'rba'].groupby(["system"]).agg(metrics)))

print("================ ISWC ================")
print(stringify_groupby(df[df['base_scenario'] == 'iswc'].groupby(["system"]).agg(metrics)))



print(stringify_groupby(df[df['group'] != 'real_world'].groupby(["system"]).agg(metrics)))
results = df.groupby(["group", "system"]).agg(metrics).applymap(lambda x: round(x, 2))
results = results.reset_index()
print(results)

df = orig_data.copy()
df['inference_time'] = df['inference_time'].apply(lambda x: x/60)
results = df.groupby(["group", "base_scenario", "scenario", "system"]).agg({
    "inference_time": ["mean"]
}).applymap(lambda x: round(x, 2))
results = results.reset_index()
# results[("inference_time", "mean")] = results[("inference_time", "mean")].apply(format_time)
# print(results)
print("\n\n")
