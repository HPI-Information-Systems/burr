import pandas as pd
import wandb
import argparse
from tqdm import tqdm
import ast

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tags", required=True, nargs='+', help="Tags of experiments to be loaded")
args = vars(ap.parse_args())
print(args)
tags = args["tags"]

api = wandb.Api()
# Project is specified by <entity/project-name>
filters = {"tags": {"$in": tags}}
runs = api.runs("lasklu/rdb2onto", filters=filters)

summary_list, config_list, name_list, tag_list, state_list = [], [], [], [], []
for run in runs: 
    # .summary contains the output keys/values for metrics like accuracy.
    #  We call ._json_dict to omit large files 
    summary_list.append(run.summary._json_dict)
    tag_list.append(run.tags)
    state_list.append(run.state)
    # .config contains the hyperparameters.
    #  We remove special values that start with _.
    config_list.append(
        {k: v for k,v in run.config.items()
          if not k.startswith('_')})

    # .name is the human-readable name of the run.
    name_list.append(run.name)


#tag = "similar_sampling"
for tag in tags:#, "similar_sampling"]:
    runs_df = pd.DataFrame({
    "summary": summary_list,
    "config": config_list,
    "name": name_list,
    "tags": tag_list,
    "state": state_list
    })
    print(runs_df.columns)

    runs_df = runs_df[runs_df["tags"].apply(lambda x: tag in x[0])]
    runs_df = runs_df[runs_df["state"] == "finished"]
    for col in runs_df.columns:
        if col in ["summary", "config"]:
            runs_df = pd.concat([runs_df.drop([col], axis=1), runs_df[col].apply(pd.Series)], axis=1)
    runs_df["tags"] = runs_df["tags"].apply(lambda x: x[0])
    def flat_dict(df, col, prefix):
        metrics_df = df[col].apply(pd.Series)
        metrics_df = metrics_df.add_prefix(f'{prefix}_')
        df = pd.concat([df, metrics_df], axis=1)
        df = df.drop(columns=[col])
        return df
    runs_df = flat_dict(runs_df, "mapping_based", "m")
    runs_df = flat_dict(runs_df, "name_based", "n")
    runs_df.to_csv(f"./experimental_evaluation/experimental_results/runs_{tag}.csv")