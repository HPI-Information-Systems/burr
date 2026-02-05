systems = {
        "rdb2onto": {
            "requires_pks": True,
            "train": {
            },
            "test": {
                "output_path": "./output/rdb2onto/",
            }
        }, 
        "d2rmapper": {
            "requires_pks": False,
            "train": {
            },
            "test": {
                "script_path": "./d2rq/generate-mapping",
                "output_path": "./output/d2rmapper/mapping.ttl",
            }
        },
        "llama": {
            "train": {
            },
            "test": {
                "chatbot": "Qwen/Qwen3-32B",
                "output_path": "./output/qwen/mapping.ttl",
                "prompt_base_path": "./evaluator/experimenter/solutions/prompts",
                "prompt": "llama_fewshot_checklist"
            }
        },
        "chatgpt": {
            "train": {
            },
            "test": {
                # "chatbot": "gpt-4.1-2025-04-14",
                "chatbot": "gemini-2.5-pro",
                "output_path": "./output/chatgpt/mapping.ttl",
                "prompt_base_path": "./evaluator/experimenter/solutions/prompts",
                "prompt": "simple"
            }
        }

}

scenarios = {
    # "normalized": {
    #         "first_normal_form": {
    #             "person_address": {
    #                 "sql_file": "micro_benchmark/normalized/first_normal_form/person_address/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/normalized/first_normal_form/person_address/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "second_normal_form": {
    #             "person_address": {
    #                 "sql_file": "micro_benchmark/normalized/second_normal_form/person_address/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/normalized/second_normal_form/person_address/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "third_normal_form": {
    #             "person_address": {
    #                 "sql_file": "micro_benchmark/normalized/third_normal_form/person_address/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/normalized/third_normal_form/person_address/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "multiple_concepts_same_table": {
    #             "library": {
    #                 "sql_file": "micro_benchmark/normalized/multiple_concepts_same_table/library/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/normalized/multiple_concepts_same_table/library/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "person_organization": {
    #                 "sql_file": "micro_benchmark/normalized/multiple_concepts_same_table/person_organization/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/normalized/multiple_concepts_same_table/person_organization/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "redundancy": {
    #             "person_address": {
    #                 "sql_file": "micro_benchmark/normalized/redundancy/person_address/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/normalized/redundancy/person_address/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "same_concept_in_same_table": {
    #             "friendship": {
    #                 "sql_file": "micro_benchmark/normalized/same_concept_in_same_table/friendship/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/normalized/same_concept_in_same_table/friendship/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "same_concept_multiple_tables": {
    #             "library": {
    #                 "sql_file": "micro_benchmark/normalized/same_concept_multiple_tables/library/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/normalized/same_concept_multiple_tables/library/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },


    #     },
    # "complex": {
    #     "scenario_a": {
    #         "friendship": {
    #             "sql_file": "micro_benchmark/complex/scenario_a/friendship/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/complex/scenario_a/friendship/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "scenario_b": {
    #         "university": {
    #             "sql_file": "micro_benchmark/complex/scenario_b/university/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/complex/scenario_b/university/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "scenario_c": {
    #         "beverage_supplier": {
    #             "sql_file": "micro_benchmark/complex/scenario_c/beverage_supplier/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/complex/scenario_c/beverage_supplier/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "component_supplier": {
    #             "sql_file": "micro_benchmark/complex/scenario_c/component_supplier/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/complex/scenario_c/component_supplier/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "scenario_d": {
    #         "hotel": {
    #             "sql_file": "micro_benchmark/complex/scenario_d/hotel/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/complex/scenario_d/hotel/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "scenario_e": {
    #         "paper": {
    #             "sql_file": "micro_benchmark/complex/scenario_e/paper/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/complex/scenario_e/paper/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "scenario_f": {
    #         "reviewer": {
    #             "sql_file": "micro_benchmark/complex/scenario_f/reviewer/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/complex/scenario_f/reviewer/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    # },
    # "attributes": {
        
    #     "cryptic_attribute_names": {
    #         "person": {
    #             "sql_file": "micro_benchmark/attributes/cryptic_attribute_names/person/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/attributes/cryptic_attribute_names/person/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
        
    #     "boolean_relation": {
    #         "beverages": {
    #             "sql_file": "micro_benchmark/attributes/boolean_relation/beverages/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/attributes/boolean_relation/beverages/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "process": {
    #             "sql_file": "micro_benchmark/attributes/boolean_relation/process/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/attributes/boolean_relation/process/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "software": {
    #             "sql_file": "micro_benchmark/attributes/boolean_relation/software/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/attributes/boolean_relation/software/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "composite_attributes": {
    #         "person": {
    #             "sql_file": "micro_benchmark/attributes/composite_attributes/person/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/attributes/composite_attributes/person/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "multi_value_attributes": {
    #         "hobbies": {
    #             "sql_file": "micro_benchmark/attributes/multi_value_attributes/hobbies/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/attributes/multi_value_attributes/hobbies/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "weak_entity": {
    #         "hotel": {
    #             "sql_file": "micro_benchmark/attributes/weak_entity/hotel/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/attributes/weak_entity/hotel/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    # },
    # "one_to_n": {
    #     "binary_n1": {
    #         "product_order": {
    #             "sql_file": "micro_benchmark/one_to_n/binary_n1/product_order/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/one_to_n/binary_n1/product_order/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "binary_n1_with_extra_table": {
    #         "product_order": {
    #             "sql_file": "micro_benchmark/one_to_n/binary_n1_with_extra_table/product_order/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/one_to_n/binary_n1_with_extra_table/product_order/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "extra_attribute": {
    #             "sql_file": "micro_benchmark/one_to_n/binary_n1_with_extra_table/extra_attribute/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/one_to_n/binary_n1_with_extra_table/extra_attribute/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "binary_reflexive_n1": {
    #         "boss_employee": {
    #             "sql_file": "micro_benchmark/one_to_n/binary_reflexive_n1/boss_employee/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/one_to_n/binary_reflexive_n1/boss_employee/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
        
    # },
    # "one_to_one": {
        
    #     "binary_one_to_one_single_relation": {
    #         "marriage": {
    #             "sql_file": "micro_benchmark/one_to_one/binary_one_to_one_single_relation/marriage/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/one_to_one/binary_one_to_one_single_relation/marriage/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "binary_one_to_one_two_relations": {
    #         "marriage": {
    #             "sql_file": "micro_benchmark/one_to_one/binary_one_to_one_two_relations/marriage/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/one_to_one/binary_one_to_one_two_relations/marriage/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
        
    # },
    # "basic": {
    #     "attributes": {
    #         "person": {
    #             "sql_file": "micro_benchmark/basic/attributes/person/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/attributes/person/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     }, 
    # "no_pk_available": {

    #         "person": {
    #             "sql_file": "micro_benchmark/basic/no_pk_available/person/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/no_pk_available/person/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "company": {
    #             "sql_file": "micro_benchmark/basic/no_pk_available/company/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/no_pk_available/company/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "person_attributes": {
    #             "sql_file": "micro_benchmark/basic/no_pk_available/person_attributes/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/no_pk_available/person_attributes/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "no_fk_available": {
    #         "movie_director_simple": {
    #             "sql_file": "micro_benchmark/basic/no_fk_available/movie_director_simple/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/no_fk_available/movie_director_simple/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "movie_director_with_attributes": {
    #             "sql_file": "micro_benchmark/basic/no_fk_available/movie_director_with_attributes/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/no_fk_available/movie_director_with_attributes/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "relationship": {
    #         "movie_director_simple": {
    #             "sql_file": "micro_benchmark/basic/relationship/movie_director_simple/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/relationship/movie_director_simple/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "movie_director_with_attributes": {
    #             "sql_file": "micro_benchmark/basic/relationship/movie_director_with_attributes/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/relationship/movie_director_with_attributes/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "table": {
    #         "company": {
    #             "sql_file": "micro_benchmark/basic/table/company/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/table/company/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "person": {
    #             "sql_file": "micro_benchmark/basic/table/person/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/table/person/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "shop": {
    #             "sql_file": "micro_benchmark/basic/table/shop/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/table/shop/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "stadium": {
    #             "sql_file": "micro_benchmark/basic/table/stadium/schema.sql",
    #             "groundtruth_mapping": "micro_benchmark/basic/table/stadium/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    # },
    # "nm_tables": {
    #         "additional_attributes": {
    #             "group_1": {
    #                 "sql_file": "micro_benchmark/nm_tables/additional_attributes/group_1/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/additional_attributes/group_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "composite_keys": {
    #             "university_1": {
    #                 "sql_file": "micro_benchmark/nm_tables/composite_keys/university_1/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/composite_keys/university_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "general": {
    #             "course_requirement": {
    #                 "sql_file": "micro_benchmark/nm_tables/general/course_requirement/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/general/course_requirement/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "customer_preference": {
    #                 "sql_file": "micro_benchmark/nm_tables/general/customer_preference/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/general/customer_preference/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "customer_preference": {
    #                 "sql_file": "micro_benchmark/nm_tables/general/customer_preference/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/general/customer_preference/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "employee_skill": {
    #                 "sql_file": "micro_benchmark/nm_tables/general/employee_skill/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/general/employee_skill/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "person_conference": {
    #                 "sql_file": "micro_benchmark/nm_tables/general/person_conference/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/general/person_conference/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "product_feature": {
    #                 "sql_file": "micro_benchmark/nm_tables/general/product_feature/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/general/product_feature/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "ternary_relation": {
    #             "textbook_course_instructor": {
    #                 "sql_file": "micro_benchmark/nm_tables/ternary_relation/textbook_course_instructor/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/ternary_relation/textbook_course_instructor/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "no_constraints": {
    #             "course_requirement": {
    #                 "sql_file": "micro_benchmark/nm_tables/no_constraints/course_requirement/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/nm_tables/no_constraints/course_requirement/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #         }
    #     },
    # "hierarchy": {
    #         "complete_redundancy": {
    #             "reviewer_1": {
    #                 "database_name": "hierarchy__complete_redundancy__reviewer_1",
    #                 "sql_file": "micro_benchmark/hierarchy/complete_redundancy/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/hierarchy/complete_redundancy/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "denormalized": {
    #             "reviewer_1": {
    #                 "database_name": "hierarchy__denormalized__reviewer_1",
    #                 "sql_file": "micro_benchmark/hierarchy/denormalized/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/hierarchy/denormalized/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "normalized": {
    #             "reviewer_1": {
    #                 "database_name": "hierarchy__normalized__reviewer_1",
    #                 "sql_file": "micro_benchmark/hierarchy/normalized/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/hierarchy/normalized/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "two_tables": {
    #             "reviewer_1": {
    #                 "database_name": "hierarchy__two_tables__reviewer_1",
    #                 "sql_file": "micro_benchmark/hierarchy/two_tables/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/hierarchy/two_tables/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "each_combination": {
    #             "reviewer_1": {
    #                 "sql_file": "micro_benchmark/hierarchy/each_combination/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "micro_benchmark/hierarchy/each_combination/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         }
    #     },
    
    "real_world": {
        "mondial": {
            "fk": {
                "sql_file": "./real-world/mondial/real_world__mondial__fk.sql",
                "schema_path": "./real-world/mondial/schema_pg_fks.sql",
                "groundtruth_mapping": "./real-world/mondial/mappings",
                "meta_file_path": "./real-world/mondial/mappings/meta.json"
            },
        },
        "npd": {
            "original": {
                "sql_file": "./real-world/npd_factpages/real_world__npd__original_2.sql",
                "schema_path": "./real-world/npd_factpages/schema_real_world__npd__original.sql",
                "groundtruth_mapping": "./real-world/npd_factpages/map_d2rq.ttl",
                "meta_file_path": "./real-world/npd_factpages/meta.json"
            }
        },
        "iswc": {
            "original": {
                "sql_file": "./real-world/iswc/real_world__iswc__original.sql",
                "groundtruth_mapping": "./real-world/iswc/groundtruth.ttl",
                "meta_file_path": "./real-world/iswc/meta.json"
            }
        },
        
        "rba": {
            "original": {
                "sql_file": "./real-world/rba/create.sql",
                "groundtruth_mapping": "./real-world/rba/mappings",
                "meta_file_path": "./real-world/rba/mappings/meta.json"
            }
        },
    }
    
    }

experiment_config = {
    "iterations": 1,
    "rewrite_database": True,
    "scenarios": scenarios,
    "systems": [
        {
            "name": "d2rmapper",
            "config": systems["d2rmapper"]
        },
        # {
        #     "name": "rdb2onto",
        #     "config": systems["rdb2onto"]
        # },
        # {
        #     "name": "chatgpt",
        #     "config": systems["chatgpt"]
        # },
        # {
        #     "name": "llama",
        #     "config": systems["llama"]
        # },
    ]
}

dynamic_config = lambda scenario, system: { "scenarios": scenario, "systems": [ { "name": system, "config": systems[system] } ] }

experiment_configs = {
    "base_experiment": experiment_config,
}