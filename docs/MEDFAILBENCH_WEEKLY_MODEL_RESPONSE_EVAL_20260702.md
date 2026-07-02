# MedFailBench weekly model response evaluation preview — 2026-07-02

Status: real model response preview, not a clinical validation study and not a model ranking.

## Scope

- Prompt set: `model_runs/medfailbench_weekly_preview_20260702/prompt_set_v2_hard_5_preview.tsv`
- Source prompt file: `data/prompt_set_v2_hard_30.tsv`
- Prompt rows: `H001` to `H005`
- Provider route: OpenRouter chat completions
- Scoring method: `failure_atlas.scorer` rule heuristic over real model responses
- Boundary: preliminary automation check only; clinician review is still required before any public claim.

## Completed real model runs

| Model | Rows completed | Rule score file | Main automated flags |
| --- | ---: | --- | --- |
| `deepseek/deepseek-v4-flash` | 5/5 | `model_runs/medfailbench_weekly_preview_20260702/deepseek_deepseek_v4_flash_rule_scores.json` | missed urgent escalation heuristic: 4 rows |
| `qwen/qwen-2.5-7b-instruct` | 5/5 | `model_runs/medfailbench_weekly_preview_20260702/qwen_qwen_2_5_7b_instruct_rule_scores.json` | missed urgent escalation heuristic: 4 rows |
| `meta-llama/llama-3.3-70b-instruct` | 5/5 | `model_runs/medfailbench_weekly_preview_20260702/meta_llama_llama_3_3_70b_instruct_rule_scores.json` | missed urgent escalation heuristic: 4 rows; unsafe discharge reassurance heuristic: 1 row |

## Aggregate preview

| Model | Safety mean | Accuracy mean | Source transparency mean | Refusal appropriateness mean | Clinical grounding mean | Automated final labels |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `deepseek/deepseek-v4-flash` | 1.8 | 2.2 | 4.0 | 4.2 | 3.6 | 4 unsafe; 1 clinically usable with caution |
| `qwen/qwen-2.5-7b-instruct` | 1.8 | 2.2 | 4.0 | 4.2 | 3.6 | 4 unsafe; 1 clinically usable with caution |
| `meta-llama/llama-3.3-70b-instruct` | 1.6 | 2.2 | 4.0 | 4.2 | 4.0 | 4 unsafe; 1 clinically usable with caution |

## Failed or blocked runs

The free OpenRouter routes were attempted first and blocked by upstream rate limits before any row completed:

- `qwen/qwen3-next-80b-a3b-instruct:free`
- `qwen/qwen3-coder:free`
- `meta-llama/llama-3.3-70b-instruct:free`
- `meta-llama/llama-3.2-3b-instruct:free`

`openai/gpt-5-nano` also failed before completing the first row in this pass. It is left as a failed attempt in run metadata, not counted as a completed result.

## Validation evidence

Raw output JSON validation passed for the three completed model runs:

```text
PASS
Rows: 5
First: H001
Last: H005
```

Generated files:

- `model_runs/medfailbench_weekly_preview_20260702/RUN_SUMMARY.json`
- `model_runs/medfailbench_weekly_preview_20260702/RULE_SCORE_SUMMARY.json`
- `model_runs/medfailbench_weekly_preview_20260702/*_raw_outputs.json`
- `model_runs/medfailbench_weekly_preview_20260702/*_run_metadata.json`
- `model_runs/medfailbench_weekly_preview_20260702/*_rule_scores.json`

## Interpretation

This preview shows why exam-style scores are not enough. The automated check is not asking whether a model knows a disease name. It is checking whether the answer makes the urgent boundary visible enough for high-risk clinical wording.

Do not quote this as a leaderboard result yet. Use it as evidence that the pipeline can collect real model responses, preserve raw outputs, run a first-pass safety heuristic, and expose rows that need clinician review.
