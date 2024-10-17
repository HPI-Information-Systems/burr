systems = {
        "rdb2onto": {
            "train": {
            },
            "test": {
                "output_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto/"
            }
        }
    }

scenarios = {
    "scenario1": {
        "attributes__fk_pk_descriptive__receipt": {
            "sql_file": "train_data/attributes/fk_pk_descriptive/receipt/schema.sql",
            "groundtruth_mapping": "train_data/attributes/fk_pk_descriptive/receipt/mapping.json",
            "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
        }
    }
}

experiment_config = {
    "scenarios": scenarios,
    "systems": [
        {
            "name": "rdb2onto",
            "config": systems["rdb2onto"]
        }
    ]
}

experiment_configs = {
    "base_experiment": experiment_config
}