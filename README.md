# Burr: A Benchmark for Ontology Learning from Relational Databases
Knowledge graphs and ontologies play an essential role in integrating, standardizing, and reasoning about complex data across domains. Leveraging knowledge graphs in AI use cases, instead of traditional relational databases, leads to quality improvements by up to 38 percentage points. However, learning ontologies from relational databases remains a challenging task due to the impedance mismatch between both modeling concepts. An understanding of which ontology learning system performs best, and why, is missing, as no standardized evaluation has been conducted.
We present Burr, a benchmark for evaluating ontology learning systems from relational databases. To evaluate the ontology learning space, we introduce a novel mapping-based evaluation metric, and provide a comprehensive benchmark data collection. This collection of 46 scenarios consists of real-world database-ontology mappings, including industry data from SAP, and of a micro-benchmark evaluating the behavior of systems in encapsulated scenarios. We demonstrate the applicability of Burr by evaluating three widely used ontology learning systems using the benchmark. The results emphasize the current strengths of simple rule-based approaches compared to LLM-based systems, while also highlighting the significant research potential of LLMs in ontology learning.

# Usage
To use Burr, please execute the command ``docker compose up burr --build``. All experiments will run automatically and can be configured in ``config_template.py``.

You have to set the following env-variables (``.env``):
```
WANDB_API_KEY=
OPENAI_API_KEY=
HF_TOKEN=
GEMINI_API_KEY=

POSTGRES_DB=postgres
POSTGRES_USER=user
POSTGRES_PASSWORD=password

WANDB_PROJECT=
WANDB_ENTITY=

SCENARIO=base_experiment
TAG=test
USE_WANDB=true

CUDA_VISIBLE_DEVICES=0
```

# Updated Evaluation Results
Values updated after correcting a small number of missing database constraints in Mondial and NPD; evaluation setup and relative system rankings are unchanged.

| Dataset | System    | Mapping (C) | Mapping (R) | Mapping (A) | Lexical (C) | Lexical (R) | Lexical (A) |
|---------|-----------|-------------|-------------|-------------|-------------|-------------|-------------|
| Mondial | Ontop     | 0.56        | 0.28        | 0.51        | 0.38        | 0.00        | 0.35        |
| Mondial | RDB2Onto  | 0.54        | 0.31        | 0.67        | 0.41        | 0.02        | 0.45        |
| NPD     | Ontop     | 0.85        | 0.85        | 0.48        | 0.06        | 0.00        | 0.00        |
| NPD     | RDB2Onto  | 0.70        | 0.81        | 0.49        | 0.06        | 0.00        | 0.00        |


# Benchmark files
This section describes the structure of the benchmark files and how to use them. The micro benchmark is split into multiple parts, each having one folder. The files can be found in folder ``micro_benchmark``.
The real world databases and their mappings can be found in the folder ``real_world``. 
Each test scenario consists of two files: 
* *SQL-File* This file includes the definition of the database and in most cases some instance data
* *Mapping file* This file represents the mapping of the database to the ontology. For better readability, we decided to choose a ``JSON`` format, which is automatically translated to ``D2RQ``.

# Architecture
![](./benchmark_architecture.png)
