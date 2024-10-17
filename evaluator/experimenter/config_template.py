rdb2onto = {
    "train": {

    },
    "test": {

    }
}

scenarios = {
    "scenario1": {
        "one": {
            "sql_file": "sql_file.sql",
            "groundtruth_mapping": "groundtruth_mapping.ttl"
        }
    }
}

experiment_config = {
    "scenarios": scenarios,
    "systems": [
        {
            "name": "rdb2onto",
            "config": rdb2onto
        }
    ]
}