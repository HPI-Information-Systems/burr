from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List

from hamilton.topic_extractors.base_topic_extractor import BaseTopicExtractor
from evaluator.database.sql_engine.table_context import DatabaseSchema

class LLMTopicExtractor(BaseTopicExtractor):
    def __init__(self, llm="google/gemma-2b-it") -> None:
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
        self.model = AutoModelForCausalLM.from_pretrained(llm)
        self.model.to(self.device)

    def extract(self, database_schema: DatabaseSchema) -> List[str]:
        database_schema_text = self.get_prompt + " " + database_schema.stringify()
        input_ids = self.tokenizer(database_schema_text, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**input_ids, max_length=5000)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    def get_prompt(self):
        return "Given the database schema, generate a list of topics that describe the data. Consider all relations. Output a json format with the topics being the keys and the values being the tables."