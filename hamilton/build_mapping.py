from evaluator.database.sql_engine.sql import DatabaseSchema, SQLEngine
from hamilton.topic_extractors.llm_topic_extractor import LLMTopicExtractor
from hamilton.interaction.dummy_interaction import DummyInteractionModule

#relation_extractor = RelationExtractor()

database_schema: DatabaseSchema = SQLEngine("TODO", "TODO").database_schema
topic_extractor = LLMTopicExtractor() #openai api / some other language model
interaction_module = DummyInteractionModule()

topics = topic_extractor.extract(database_schema)
topics = interaction_module.feedback_from_user(topics)
# user returns relations and changes to topics, so we have a list which table belongs to which topic and how topics relate to each other
# now we iterate over the topics and build a detailed mapping. ->   
mapping = Mapping()
for topic in topics:
    topic_cluster = refine_topic(topic)
    topic_cluster = feedback_from_user(topic_cluster)
    mapping.add_topic_cluster(topic_cluster)
