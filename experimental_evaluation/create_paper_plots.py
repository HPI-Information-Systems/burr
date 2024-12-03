import pandas as pd
latex_template = r"""
\begin{table*}[t!]
\centering 
\setlength{\tabcolsep}{3pt}
\begin{tabular}{l|ccc|ccc|ccc|ccc|ccc|ccc}\toprule
System & \multicolumn{6}{c|}{\textsc{W3C-Mapper}} & \multicolumn{6}{c|}{\textsc{RDB2Onto}}  & \multicolumn{6}{c}{\textsc{OntoGenix}} \\ 
Metric & \multicolumn{3}{c|}{Mapping} & \multicolumn{3}{c|}{Lexical}   & \multicolumn{3}{c|}{Mapping} & \multicolumn{3}{c|}{Lexical} & \multicolumn{3}{c|}{Mapping} & \multicolumn{3}{c}{Lexical} \\ 
Element & \multicolumn{1}{c}{Conc.}     & \multicolumn{1}{c}{Rel.}   & \multicolumn{1}{c|}{Attr.} & \multicolumn{1}{c}{Conc.}     & \multicolumn{1}{c}{Rel.}   & \multicolumn{1}{c|}{Attr.}& \multicolumn{1}{c}{Conc.}     & \multicolumn{1}{c}{Rel.}   & \multicolumn{1}{c|}{Attr.}& \multicolumn{1}{c}{Conc.}     & \multicolumn{1}{c}{Rel.}   & \multicolumn{1}{c|}{Attr.}& \multicolumn{1}{c}{Conc.}     & \multicolumn{1}{c}{Rel.}   & \multicolumn{1}{c|}{Attr.}& \multicolumn{1}{c}{Conc.}     & \multicolumn{1}{c}{Rel.}   & \multicolumn{1}{c}{Attr.} \\ \midrule
\multicolumn{18}{c}{Real-World Scenarios} \\\midrule
{real_world_rows}
\\\midrule
\multicolumn{18}{c}{Micro Benchmark} \\\midrule
{micro_benchmark_rows}
\bottomrule
\end{tabular}
	\captionWithDescription{Quality Overview per Scenario and System executed on \system}{All results are $F_1$-score. Results are divided into how well concepts (Conc.), relations (Attr.) and attributes (Rel.) can be extracted.}
	\label{tab: results}
\end{table*}
"""
# Example DataFrame (replace with your real data)
data = {
    'System': ['Mondial', 'Mondial-FK', 'Enterprise', 'ISWC'],
    'Conc.': [0.45, 0.45, 0.00, 0.53],
    'Rel.': [0.00, 0.40, 0.00, 0.11],
    'Attr.': [0.52, 0.52, 0.54, 0.48],
    'Conc_Lexical': [0.38, 0.38, 0.00, 0.00],
    'Rel_Lexical': [0.00, 0.00, 0.00, 0.00],
    'Attr_Lexical': [0.38, 0.38, 0.00, 0.00],
}
df = pd.DataFrame(data)

# Generate rows dynamically
def generate_rows(df):
    rows = []
    for _, row in df.iterrows():
        rows.append(
            f"{row['System']} & {row['Conc.']} & {row['Rel.']} & {row['Attr.']} & "
            f"{row['Conc_Lexical']} & {row['Rel_Lexical']} & {row['Attr_Lexical']} \\\\"
        )
    return "\n".join(rows)

# Populate specific sections
real_world_rows = generate_rows(df)  # Adjust the dataframe for "Real-World Scenarios"
micro_benchmark_rows = generate_rows(df)  # Adjust for "Micro Benchmark"

# Fill the template
latex_output = latex_template.format(
    real_world_rows=real_world_rows,
    micro_benchmark_rows=micro_benchmark_rows
)

# Save to file
with open("table.tex", "w") as f:
    f.write(latex_output)