# KORA model-diversity results (N=330, judge=Sonnet 4.6 fixed)

| Model | tier | deflection | LLM calls saved | with-KB d-acc | without-KB d-acc |
|---|---|---|---|---|---|
| Llama 3.1 8B | tiny | 76.7% | 76.7% | +0.123 | +0.335 |
| Llama 3.3 70B | large | 76.7% | 76.7% | +0.050 | +0.319 |
| Claude Haiku 4.5 | small | 76.7% | 76.7% | +0.019 | +0.300 |
| Nova Pro | mid | 76.7% | 76.7% | +0.031 | +0.265 |
| Claude Sonnet 4.6 | frontier | 76.7% | 76.7% | +0.012 | +0.223 |

- **deflection 76.7% identical across all models** (set by the deterministic router, model-independent)
- **without-KB**: direct varies with model strength; KORA stays ~0.98 -> larger gain for weaker models
- over-routed: 2 cases (routing precision=0.883)