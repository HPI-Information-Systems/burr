systems = {
        "rdb2onto": {
            "requires_pks": True,
            "train": {
            },
            "test": {
                "output_path": "./output/rdb2onto/",
            }
        }, 
        "ontogenix": {
            "train": {
            },
            "test": {
                "chatbot": "gpt-4o",
                # "chatbot": "gpt-4o-mini",
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
        }   
}

single_scenario = {
    "nm_tables": {
        "trinary_relation": {
                "student_instructor_1": {
                    #"database_name": "hierarchy__two_tables__reviewer_1",
                    "sql_file": "train_data/nm_tables/trinary_relation/student_instructor_1/schema.sql",
                    "groundtruth_mapping": "train_data/nm_tables/trinary_relation/student_instructor_1/mapping.json",
                    "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
                },
        }
    }
}

scenarios = {
    # "attributes": {
        
    #     "cryptic_attribute_names": {
    #         "person": {
    #             "sql_file": "train_data/attributes/cryptic_attribute_names/person/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/cryptic_attribute_names/person/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "no_pk_available": {
    #         "person": {
    #             "sql_file": "train_data/attributes/no_pk_available/person/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/no_pk_available/person/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "company": {
    #             "sql_file": "train_data/attributes/no_pk_available/company/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/no_pk_available/company/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "person_attributes": {
    #             "sql_file": "train_data/attributes/no_pk_available/person_attributes/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/no_pk_available/person_attributes/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "no_fk_available": {
    #         "movie_director_simple": {
    #             "sql_file": "train_data/attributes/no_fk_available/movie_director_simple/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/no_fk_available/movie_director_simple/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "movie_director_with_attributes": {
    #             "sql_file": "train_data/attributes/no_fk_available/movie_director_with_attributes/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/no_fk_available/movie_director_with_attributes/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "boolean_relation": {
    #         "beverages": {
    #             "sql_file": "train_data/attributes/boolean_relation/beverages/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/boolean_relation/beverages/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "process": {
    #             "sql_file": "train_data/attributes/boolean_relation/process/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/boolean_relation/process/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "software": {
    #             "sql_file": "train_data/attributes/boolean_relation/software/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/boolean_relation/software/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "composite_attributes": {
    #         "person": {
    #             "sql_file": "train_data/attributes/composite_attributes/person/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/composite_attributes/person/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "multi_value_attributes": {
    #         "hobbies": {
    #             "sql_file": "train_data/attributes/multi_value_attributes/hobbies/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/multi_value_attributes/hobbies/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    #     "weak_entity": {
    #         "hotel": {
    #             "sql_file": "train_data/attributes/weak_entity/hotel/schema.sql",
    #             "groundtruth_mapping": "train_data/attributes/weak_entity/hotel/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         }
    #     },
    # },
    # "one_to_n": {
    #     "binary_n1": {
    #         "product_order": {
    #             "sql_file": "train_data/one_to_n/binary_n1/product_order/schema.sql",
    #             "groundtruth_mapping": "train_data/one_to_n/binary_n1/product_order/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "binary_n1_with_extra_table": {
    #         "product_order": {
    #             "sql_file": "train_data/one_to_n/binary_n1_with_extra_table/product_order/schema.sql",
    #             "groundtruth_mapping": "train_data/one_to_n/binary_n1_with_extra_table/product_order/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "extra_attribute": {
    #             "sql_file": "train_data/one_to_n/binary_n1_with_extra_table/extra_attribute/schema.sql",
    #             "groundtruth_mapping": "train_data/one_to_n/binary_n1_with_extra_table/extra_attribute/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "binary_reflexive_n1": {
    #         "boss_employee": {
    #             "sql_file": "train_data/one_to_n/binary_reflexive_n1/boss_employee/schema.sql",
    #             "groundtruth_mapping": "train_data/one_to_n/binary_reflexive_n1/boss_employee/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     
    # },
    # "one_to_one": {
        
    #     "binary_one_to_one_single_relation": {
    #         "marriage": {
    #             "sql_file": "train_data/one_to_one/binary_one_to_one_single_relation/marriage/schema.sql",
    #             "groundtruth_mapping": "train_data/one_to_one/binary_one_to_one_single_relation/marriage/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    #     "binary_one_to_one_two_relations": {
    #         "marriage": {
    #             "sql_file": "train_data/one_to_one/binary_one_to_one_two_relations/marriage/schema.sql",
    #             "groundtruth_mapping": "train_data/one_to_one/binary_one_to_one_two_relations/marriage/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
        
    # },
    # "basic": {
    #     # "attributes": {
    #     #     "person": {
    #     #         "sql_file": "train_data/basic/attributes/person/schema.sql",
    #     #         "groundtruth_mapping": "train_data/basic/attributes/person/mapping.json",
    #     #         "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #     #     }
    #     # },
    #     # "relationship": {
    #     #     "movie_director_simple": {
    #     #         "sql_file": "train_data/basic/relationship/movie_director_simple/schema.sql",
    #     #         "groundtruth_mapping": "train_data/basic/relationship/movie_director_simple/mapping.json",
    #     #         "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #     #     },
    #     #     "movie_director_with_attributes": {
    #     #         "sql_file": "train_data/basic/relationship/movie_director_with_attributes/schema.sql",
    #     #         "groundtruth_mapping": "train_data/basic/relationship/movie_director_with_attributes/mapping.json",
    #     #         "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #     #     },
    #     # },
    #     "table": {
    #         "company": {
    #             "sql_file": "train_data/basic/table/company/schema.sql",
    #             "groundtruth_mapping": "train_data/basic/table/company/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "person": {
    #             "sql_file": "train_data/basic/table/person/schema.sql",
    #             "groundtruth_mapping": "train_data/basic/table/person/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "shop": {
    #             "sql_file": "train_data/basic/table/shop/schema.sql",
    #             "groundtruth_mapping": "train_data/basic/table/shop/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #         "stadium": {
    #             "sql_file": "train_data/basic/table/stadium/schema.sql",
    #             "groundtruth_mapping": "train_data/basic/table/stadium/mapping.json",
    #             "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #         },
    #     },
    # },
    # "nm_tables": {
    #         "additional_attributes": {
    #             "group_1": {
    #                 "sql_file": "train_data/nm_tables/additional_attributes/group_1/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/additional_attributes/group_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "composite_keys": {
    #             "university_1": {
    #                 "sql_file": "train_data/nm_tables/composite_keys/university_1/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/composite_keys/university_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "general": {
    #             "course_requirement": {
    #                 "sql_file": "train_data/nm_tables/general/course_requirement/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/general/course_requirement/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "customer_preference": {
    #                 "sql_file": "train_data/nm_tables/general/customer_preference/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/general/customer_preference/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "customer_preference": {
    #                 "sql_file": "train_data/nm_tables/general/customer_preference/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/general/customer_preference/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "employee_skill": {
    #                 "sql_file": "train_data/nm_tables/general/employee_skill/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/general/employee_skill/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "person_conference": {
    #                 "sql_file": "train_data/nm_tables/general/person_conference/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/general/person_conference/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "product_feature": {
    #                 "sql_file": "train_data/nm_tables/general/product_feature/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/general/product_feature/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "ternary_relation": {
    #             "student_instructor_1": {
    #                 "sql_file": "train_data/nm_tables/ternary_relation/student_instructor_1/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/ternary_relation/student_instructor_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "no_constraints": {
    #             "course_requirement": {
    #                 "sql_file": "train_data/nm_tables/no_constraints/course_requirement/schema.sql",
    #                 "groundtruth_mapping": "train_data/nm_tables/no_constraints/course_requirement/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #         }
    #     },
    # "normalized": {
    #         "first_normal_form": {
    #             "person_address": {
    #                 "sql_file": "train_data/normalized/first_normal_form/person_address/schema.sql",
    #                 "groundtruth_mapping": "train_data/normalized/first_normal_form/person_address/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "second_normal_form": {
    #             "person_address": {
    #                 "sql_file": "train_data/normalized/second_normal_form/person_address/schema.sql",
    #                 "groundtruth_mapping": "train_data/normalized/second_normal_form/person_address/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "third_normal_form": {
    #             "person_address": {
    #                 "sql_file": "train_data/normalized/third_normal_form/person_address/schema.sql",
    #                 "groundtruth_mapping": "train_data/normalized/third_normal_form/person_address/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "multiple_concepts_same_table": {
    #             "library": {
    #                 "sql_file": "train_data/normalized/multiple_concepts_same_table/library/schema.sql",
    #                 "groundtruth_mapping": "train_data/normalized/multiple_concepts_same_table/library/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             },
    #             "person_organization": {
    #                 "sql_file": "train_data/normalized/multiple_concepts_same_table/person_organization/schema.sql",
    #                 "groundtruth_mapping": "train_data/normalized/multiple_concepts_same_table/person_organization/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "redundancy": {
    #             "person_address": {
    #                 "sql_file": "train_data/normalized/redundancy/person_address/schema.sql",
    #                 "groundtruth_mapping": "train_data/normalized/redundancy/person_address/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "same_concept_in_same_table": {
    #             "friendship": {
    #                 "sql_file": "train_data/normalized/same_concept_in_same_table/friendship/schema.sql",
    #                 "groundtruth_mapping": "train_data/normalized/same_concept_in_same_table/friendship/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "same_concept_multiple_tables": {
    #             "library": {
    #                 "sql_file": "train_data/normalized/same_concept_multiple_tables/library/schema.sql",
    #                 "groundtruth_mapping": "train_data/normalized/same_concept_multiple_tables/library/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },


    #     },
    # "hierarchy": {
    #         "complete_redundancy": {
    #             "reviewer_1": {
    #                 "database_name": "hierarchy__complete_redundancy__reviewer_1",
    #                 "sql_file": "train_data/hierarchy/complete_redundancy/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "train_data/hierarchy/complete_redundancy/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "denormalized": {
    #             "reviewer_1": {
    #                 "database_name": "hierarchy__denormalized__reviewer_1",
    #                 "sql_file": "train_data/hierarchy/denormalized/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "train_data/hierarchy/denormalized/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "normalized": {
    #             "reviewer_1": {
    #                 "database_name": "hierarchy__normalized__reviewer_1",
    #                 "sql_file": "train_data/hierarchy/normalized/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "train_data/hierarchy/normalized/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "two_tables": {
    #             "reviewer_1": {
    #                 "database_name": "hierarchy__two_tables__reviewer_1",
    #                 "sql_file": "train_data/hierarchy/two_tables/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "train_data/hierarchy/two_tables/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         },
    #         "each_combination": {
    #             "reviewer_1": {
    #                 "sql_file": "train_data/hierarchy/each_combination/reviewer_1/schema.sql",
    #                 "groundtruth_mapping": "train_data/hierarchy/each_combination/reviewer_1/mapping.json",
    #                 "meta_file_path": "./evaluator/mapping_parser/d2rq_mapping/base_meta.json"
    #             }
    #         }
    #     },
    "real_world": {
        # "rba": {
        #     "original": {
        #         "sql_file": "./real-world/rba/create.sql",
        #         "groundtruth_mapping": "./real-world/rba/mappings",
        #         "meta_file_path": "./real-world/rba/mappings/meta.json"
        #     },
        # },
        # "mondial": {
        #     "original": {
        #         "sql_file": "./real-world/mondial/real_world__mondial__original.sql",
        #         "groundtruth_mapping": "./real-world/mondial/mappings",
        #         "meta_file_path": "./real-world/mondial/mappings/meta.json"
        #     },
        #     "fk": {
        #         "sql_file": "./real-world/mondial/real_world__mondial__fk.sql",
        #         "groundtruth_mapping": "./real-world/mondial/mappings",
        #         "meta_file_path": "./real-world/mondial/mappings/meta.json"
        #     }
        # },
        # "iswc": {
        #     "original": {
        #         "sql_file": "./real-world/iswc/real_world__iswc__original.sql",
        #         "groundtruth_mapping": "./real-world/iswc/groundtruth.ttl",
        #         "meta_file_path": "./real-world/iswc/meta.json"
        #     }
        # },
        "apqc": {
            "original": {
                "sql_file": "./real-world/apqc/apqc.sql",
                "groundtruth_mapping": "./real-world/apqc/mappings",
                "meta_file_path": "./real-world/apqc/mappings/meta.json"
            },
        }
    }
    
    }

experiment_config = {
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
        #     "name": "ontogenix",
        #     "config": systems["ontogenix"]
        # }
    ]
}

dynamic_config = lambda scenario, system: { "scenarios": scenario, "systems": [ { "name": system, "config": systems[system] } ] }

experiment_configs = {
    "base_experiment": experiment_config,
    "single_scenario": dynamic_config(single_scenario, "d2rmapper")
}