systems = {
        "rdb2onto": {
            "train": {
            },
            "test": {
                "output_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/output/rdb2onto/"
            }
        }
    }

single_scenario = {
    "nm_tables": {
        "trinary_relation": {
                "student_instructor_1": {
                    #"database_name": "hierarchy__two_tables__reviewer_1",
                    "sql_file": "train_data/nm_tables/trinary_relation/student_instructor_1/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/trinary_relation/student_instructor_1/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
        }
    }
}

scenarios = {
    "attributes": {
        "fk_pk_descriptive": {
            "receipt": {
                "database_name": "attributes__fk_pk_descriptive__receipt",
                "sql_file": "train_data/attributes/fk_pk_descriptive/receipt/schema.sql",
                "groundtruth_mapping": "train_data/attributes/fk_pk_descriptive/receipt/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            },
            
        },
        "table_checks": {
            "adult": {
                "sql_file": "train_data/attributes/table_checks/adult/schema.sql",
                "groundtruth_mapping": "train_data/attributes/table_checks/adult/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            }
        },
        "cryptic_attribute_names": {
            "person": {
                "sql_file": "train_data/attributes/cryptic_attribute_names/person/schema.sql",
                "groundtruth_mapping": "train_data/attributes/cryptic_attribute_names/person/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            }
        },
    },
    "basic": {
        "attributes": {
            "person": {
                "sql_file": "train_data/basic/attributes/person/schema.sql",
                "groundtruth_mapping": "train_data/basic/attributes/person/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            }
        },
        "relationship": {
            "movie_director_simple": {
                "sql_file": "train_data/basic/relationship/movie_director_simple/schema.sql",
                "groundtruth_mapping": "train_data/basic/relationship/movie_director_simple/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            },
            "movie_director_with_attributes": {
                "sql_file": "train_data/basic/relationship/movie_director_with_attributes/schema.sql",
                "groundtruth_mapping": "train_data/basic/relationship/movie_director_with_attributes/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            },
        },
        "table": {
            "company": {
                "sql_file": "train_data/basic/table/company/schema.sql",
                "groundtruth_mapping": "train_data/basic/table/company/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            },
            "person": {
                "sql_file": "train_data/basic/table/person/schema.sql",
                "groundtruth_mapping": "train_data/basic/table/person/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            },
            "shop": {
                "sql_file": "train_data/basic/table/shop/schema.sql",
                "groundtruth_mapping": "train_data/basic/table/shop/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            },
            "stadium": {
                "sql_file": "train_data/basic/table/stadium/schema.sql",
                "groundtruth_mapping": "train_data/basic/table/stadium/mapping.json",
                "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
            },
        },
    "denormalized": {
        "boolean_relation": {
                "beverages": {
                    "sql_file": "train_data/denormalized/boolean_relation/beverages/schema.sql",
                    "groundtruth_mapping": "train_data/denormalized/boolean_relation/beverages/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
                "process": {
                        "sql_file": "train_data/denormalized/boolean_relation/process/schema.sql",
                        "groundtruth_mapping": "train_data/denormalized/boolean_relation/process/mapping.json",
                        "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
                "software": {
                        "sql_file": "train_data/denormalized/boolean_relation/software/schema.sql",
                        "groundtruth_mapping": "train_data/denormalized/boolean_relation/software/mapping.json",
                        "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "composite_attributes": {
                "person": {
                    "sql_file": "train_data/denormalized/composite_attributes/person/schema.sql",
                    "groundtruth_mapping": "train_data/denormalized/composite_attributes/person/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "multiple_concepts_same_table": {
                "library": {
                    "sql_file": "train_data/denormalized/multiple_concepts_same_table/library/schema.sql",
                    "groundtruth_mapping": "train_data/denormalized/multiple_concepts_same_table/library/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
                "person_organization": {
                    "sql_file": "train_data/denormalized/multiple_concepts_same_table/person_organization/schema.sql",
                    "groundtruth_mapping": "train_data/denormalized/multiple_concepts_same_table/person_organization/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "relation_of_concepts_in_same_table": {
                "process": {
                    "sql_file": "train_data/denormalized/relation_of_concepts_in_same_table/process/schema.sql",
                    "groundtruth_mapping": "train_data/denormalized/relation_of_concepts_in_same_table/process/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "same_concept_in_same_table": {
                "friendship": {
                    "sql_file": "train_data/denormalized/same_concept_in_same_table/friendship/schema.sql",
                    "groundtruth_mapping": "train_data/denormalized/same_concept_in_same_table/friendship/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "same_concept_multiple_tables": {
                "library": {
                    "sql_file": "train_data/denormalized/same_concept_multiple_tables/library/schema.sql",
                    "groundtruth_mapping": "train_data/denormalized/same_concept_multiple_tables/library/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            }
        },
        "nm_tables": {
            "additional_attributes": {
                "group_1": {
                    "sql_file": "train_data/nm_tables/additional_attributes/group_1/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/additional_attributes/group_1/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "composite_keys": {
                "university_1": {
                    "sql_file": "train_data/nm_tables/composite_keys/university_1/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/composite_keys/university_1/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "general": {
                "course_requirement": {
                    "sql_file": "train_data/nm_tables/general/course_requirement/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/general/course_requirement/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
                "customer_preference": {
                    "sql_file": "train_data/nm_tables/general/customer_preference/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/general/customer_preference/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
                "customer_preference": {
                    "sql_file": "train_data/nm_tables/general/customer_preference/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/general/customer_preference/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
                "employee_skill": {
                    "sql_file": "train_data/nm_tables/general/employee_skill/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/general/employee_skill/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
                "person_conference": {
                    "sql_file": "train_data/nm_tables/general/person_conference/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/general/person_conference/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
                "product_feature": {
                    "sql_file": "train_data/nm_tables/general/product_feature/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/general/product_feature/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "trinary_relation": {
                "student_instructor_1": {
                    "sql_file": "train_data/nm_tables/trinary_relation/student_instructor_1/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/trinary_relation/student_instructor_1/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            }
        },
        "normalized": {
            "strong_normalization": {
                "person_address": {
                    "sql_file": "train_data/normalized/strong_normalization/person_address/schema.sql",
                    "groundtruth_mapping": "train_data/normalized/strong_normalization/person_address/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            }
        },
        "reviewer_1_hierarchy": {
            "complete_redundancy": {
                "mapping": {
                    "database_name": "hierarchy__complete_redundancy__reviewer_1",
                    "sql_file": "train_data/reviewer_1_hierarchy/complete_redundancy/schema.sql",
                    "groundtruth_mapping": "train_data/reviewer_1_hierarchy/complete_redundancy/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "denormalized": {
                "mapping": {
                    "database_name": "hierarchy__denormalized__reviewer_1",
                    "sql_file": "train_data/reviewer_1_hierarchy/denormalized/schema.sql",
                    "groundtruth_mapping": "train_data/reviewer_1_hierarchy/denormalized/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "normalized": {
                "mapping": {
                    "database_name": "hierarchy__normalized__reviewer_1",
                    "sql_file": "train_data/reviewer_1_hierarchy/normalized/schema.sql",
                    "groundtruth_mapping": "train_data/reviewer_1_hierarchy/normalized/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            },
            "two_tables": {
                "mapping": {
                    "database_name": "hierarchy__two_tables__reviewer_1",
                    "sql_file": "train_data/reviewer_1_hierarchy/two_tables/schema.sql",
                    "groundtruth_mapping": "train_data/reviewer_1_hierarchy/two_tables/mapping.json",
                    "meta_file_path": "/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                }
            }
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

dynamic_config = lambda scenario: { "scenarios": scenario, "systems": [ { "name": "rdb2onto", "config": systems["rdb2onto"] } ] }

experiment_configs = {
    "base_experiment": experiment_config,
    "single_scenario": dynamic_config(single_scenario)
}