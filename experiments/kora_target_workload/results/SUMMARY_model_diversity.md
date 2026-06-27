# KORA 모델 다양성 결과 (N=330, judge=Sonnet 4.6 고정)

| 모델 | 체급 | deflection | LLM콜 절감 | with-KB Δacc | without-KB Δacc |
|---|---|---|---|---|---|
| Llama 3.1 8B | 극소 | 76.7% | 76.7% | +0.123 | +0.335 |
| Llama 3.3 70B | 대 | 76.7% | 76.7% | +0.050 | +0.319 |
| Claude Haiku 4.5 | 소 | 76.7% | 76.7% | +0.019 | +0.300 |
| Nova Pro | 중 | 76.7% | 76.7% | +0.031 | +0.265 |
| Claude Sonnet 4.6 | 대(frontier) | 76.7% | 76.7% | +0.012 | +0.223 |

- **deflection 76.7% 전모델 동일** (결정형 라우터가 정하므로 모델 무관)
- **without-KB**: direct는 모델 실력 따라 변동, KORA는 ~0.98로 고정 → 약한 모델일수록 이득↑
- over-routed: 2건 (routing precision=0.883)