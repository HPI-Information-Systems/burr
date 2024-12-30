import os

folder_to_mapping_files = '/Users/lukaslaskowski/Documents/HPI/KG/ontology_mappings/rdb2ontology/train_data'


maps = list(map(lambda x: os.path.basename(x), filter(lambda x: x.endswith('.json'), os.listdir(folder_to_mapping_files))))


maps = [os.path.basename(mapping_file) for mapping_file in os.listdir(folder_to_mapping_files)]


# maps = list(map(lambda x:))
