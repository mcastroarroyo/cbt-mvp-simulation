"""Minimal three-stage runner (template).
- Fills prompts with inputs and rules.
- Expects you to plug in your LLM API calls where indicated.
- Produces JSON trace files for Stage 1 and Stage 2, and a final answer text file.

IMPORTANT: Do not commit API keys. Supply them via environment variables.
"""
import os, json, pathlib, datetime

# --- Configuration (EDIT) ---
MODEL_STAGE1 = os.getenv("CBT_MODEL_STAGE1", "gpt-4o-mini")   # replace with your provider/model
MODEL_STAGE2 = os.getenv("CBT_MODEL_STAGE2", "gpt-4o-mini")
MODEL_STAGE3 = os.getenv("CBT_MODEL_STAGE3", "gpt-4o-mini")
MODEL_JUDGE  = os.getenv("CBT_MODEL_JUDGE",  "gpt-4o-mini")

TEMPERATURE = float(os.getenv("CBT_TEMPERATURE", "0.2"))
TOP_P       = float(os.getenv("CBT_TOP_P", "0.95"))
SEED        = int(os.getenv("CBT_SEED", "42"))

# --- Paths ---
BASE = pathlib.Path(__file__).resolve().parents[1]
PROMPTS = BASE / "prompts"
RULES = BASE / "rules"
EXAMPLES = BASE / "examples"
OUT = BASE / "runs"
OUT.mkdir(exist_ok=True)

def read(path): 
    with open(path, "r", encoding="utf-8") as f: 
        return f.read()

def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)

def call_llm(model, prompt, system=None):
    """PLACEHOLDER: Replace with actual LLM API call and return text output."""
    # e.g., OpenAI, Anthropic, etc. Respect TEMPERATURE, TOP_P, SEED where supported.
    raise NotImplementedError("Plug in your LLM API provider here.")

def main():
    # Load templates
    p1 = read(PROMPTS / "stage1_concept_extractor.txt")
    p2 = read(PROMPTS / "stage2_structural_reasoner.txt")
    p3 = read(PROMPTS / "stage3_guided_generator.txt")
    judge = read(PROMPTS / "judge_rubric.txt")
    rules = read(RULES / "sample_rules.yaml")
    query = read(EXAMPLES / "scenario1_input.txt")

    # Stage 1
    prompt1 = f"{p1}\n\nINPUT QUERY:\n{query}\n"
    stage1_text = call_llm(MODEL_STAGE1, prompt1)
    stage1 = json.loads(stage1_text)
    write_json(OUT / "scenario1_stage1.json", stage1)

    # Stage 2
    prompt2 = f"{p2}\n\nINPUT CONSTRUCTS JSON:\n{json.dumps(stage1)}\n\nRULES:\n{rules}\n"
    stage2_text = call_llm(MODEL_STAGE2, prompt2)
    stage2 = json.loads(stage2_text)
    write_json(OUT / "scenario1_stage2.json", stage2)

    # Stage 3
    prompt3 = f"{p3}\n\nORIGINAL QUERY:\n{query}\n\nPLAN JSON:\n{json.dumps(stage2.get('plan', {}))}\n"
    final_text = call_llm(MODEL_STAGE3, prompt3)
    with open(OUT / "scenario1_final.txt", "w", encoding="utf-8") as f:
        f.write(final_text)

    # Judge (optional)
    judge_prompt_full = f"{judge}\n\nRESPONSE:\n{final_text}\n"
    # judge_text = call_llm(MODEL_JUDGE, judge_prompt_full)
    # with open(OUT / "scenario1_judge.json", "w", encoding="utf-8") as f:
    #     f.write(judge_text)

    meta = {
        "models": {
            "stage1": MODEL_STAGE1, "stage2": MODEL_STAGE2, "stage3": MODEL_STAGE3, "judge": MODEL_JUDGE
        },
        "params": {"temperature": TEMPERATURE, "top_p": TOP_P, "seed": SEED},
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }
    write_json(OUT / "run_meta.json", meta)

if __name__ == "__main__":
    main()
