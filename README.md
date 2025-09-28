CBT MVP Simulation
This repository provides prompts, rules, example traces, and a minimal runner template for the Construct-Based Transformer (CBT) three-stage simulation:

Concept Extractor → extracts predefined constructs to JSON
Structural Reasoner → applies explicit rules over constructs
Guided Generator → produces the final answer grounded in the plan
Paper: CBT_Concept_Note_v1.pdf (paper/)

How to run
Edit construct list in prompts/stage1_concept_extractor.txt and rules in rules/sample_rules.yaml.
Open runner/min_runner.py and implement your LLM API in call_llm(...).
(Optional) Set env vars:
CBT_MODEL_STAGE1, CBT_MODEL_STAGE2, CBT_MODEL_STAGE3, CBT_MODEL_JUDGE
CBT_TEMPERATURE (default 0.2), CBT_TOP_P (default 0.95), CBT_SEED (default 42)
Run: python runner/min_runner.py
Outputs will be written to runs/.
Reproducibility fields (fill before a release)
Stage 1 model/version: …
Stage 2 model/version: …
Stage 3 model/version: …
Judge model/version: …
Sampling: temperature=…, top_p=…
Seed: …
Run date/time (UTC): …
License
Code (runner/ and any scripts): Apache-2.0 (see LICENSE-CODE)
Content (PDF, prompts, rules, examples): CC BY-NC-ND 4.0 (see LICENSE-CONTENT)
Citation
If you use this repository, please cite the Zenodo DOI for the release you used and the concept paper:

Castro Arroyo, M. A. (2025). Construct-Based Transformers: A Conceptual Architecture and MVP Simulation. (Release v1.0). Zenodo. DOI: TBA

Castro Arroyo, M. A. (2025). Construct-Based Transformers: A Conceptual Architecture and MVP Simulation. (Preprint).
