# KORA First Paper Preliminary BibTeX v0.1

## Purpose

This document contains preliminary BibTeX only for reference records that passed the ready-record check after metadata audit v0.1, normalized bibliography v0.1, and metadata gap resolution v0.1.

It is a bibliography-preparation document. It does not modify manuscript v0.3, does not include blocked records, and does not make the paper submission-ready.

## Scope

Included ready subset:

- `[R01]`
- `[R06]`
- `[R08]`
- `[R11]`
- `[R14]`
- `[R21]`
- `[R24]`

Blocked records are excluded. Manuscript v0.3 is unchanged. The paper remains not submission-ready.

## Rules

- Do not generate BibTeX for blocked records.
- Do not invent metadata.
- Do not infer venues, authors, years, DOI values, or source URLs.
- Treat these entries as preliminary and recheck them before submission.
- Keep stable `[Rxx]` labels as canonical while the audit is active.
- Defer venue-specific style conversion until the target venue or report format is chosen.

## Ready-Record Check

| ID | Topic | Ready for preliminary BibTeX | Reason | Notes |
|---|---|---|---|---|
| `[R01]` | vLLM / PagedAttention | yes | Title, full author list, year, arXiv URL, DOI, and SOSP 2023 status are present in normalized records. | Related-work context only; does not support KORA superiority over serving systems. |
| `[R06]` | Retrieval-Augmented Generation | yes | Title, full author list, year, arXiv URL, DOI, and NeurIPS 2020 status are present in normalized records. | RAG contrast only; does not imply KORA replaces retrieval-grounded generation. |
| `[R08]` | Snakemake | yes | Title, author list, year, journal/volume/pages, and DOI are present in normalized records. | Reproducible workflow background only. |
| `[R11]` | ReAct | yes | Title, full author list, year, arXiv URL, DOI, and ICLR 2023 status are present in normalized records. | Agent/tool-use context only; no KORA outperformance claim. |
| `[R14]` | GPTCache | yes | Title, author, year, ACL Anthology URL, DOI, workshop venue, publisher, and pages are present in normalized records. | Title includes cost-related wording; do not use as KORA production cost or real API-cost evidence. |
| `[R21]` | SWE-bench | yes | Title, full author list, year, arXiv URL, DOI, and ICLR 2024 status are present in normalized records. | Benchmark-construction example only; no KORA comparison against SWE-bench. |
| `[R24]` | CheckList | yes | Title, full author list, year, ACL Anthology URL, DOI, venue, and pages are present in normalized records. | Behavior-oriented evaluation design context only; does not imply broad KORA behavioral testing. |

No ready-subset record was moved back to blocked in this pass.

## BibTeX Key Normalization

| ID | Topic | Previous key | Normalized key | Key status | Reason |
|---|---|---|---|---|---|
| `[R01]` | vLLM / PagedAttention | `kwon2023pagedattention` | `kwon2023pagedattention` | normalized | First author, year, and topic are verified in the normalized bibliography and tracker; key is readable and collision-resistant enough for the current ready subset. |
| `[R06]` | Retrieval-Augmented Generation | `lewis2020rag` | `lewis2020rag` | normalized | First author, year, and RAG topic are verified; key is concise and stable. |
| `[R08]` | Snakemake | `koster2012snakemake` | `koster2012snakemake` | normalized | First author, year, and topic are verified from DOI-backed metadata; key is clear and stable. |
| `[R11]` | ReAct | `yao2023react` | `yao2023react` | normalized | First author, year, and topic are verified from the recorded arXiv/DOI metadata; key is clear and stable. |
| `[R14]` | GPTCache | `bang2023gptcache` | `bang2023gptcache` | normalized | Sole author, year, and topic are verified from ACL Anthology metadata; key is clear and stable. |
| `[R21]` | SWE-bench | `jimenez2024swebench` | `jimenez2024swebench` | normalized | First author, year, and benchmark topic are verified; key avoids punctuation while preserving the SWE-bench topic. |
| `[R24]` | CheckList | `ribeiro2020checklist` | `ribeiro2020checklist` | normalized | First author, year, and CheckList topic are verified from ACL Anthology metadata; key is clear and stable. |

All ready-subset keys already followed the selected author/year/topic pattern and were kept unchanged. Final venue key review may still adjust capitalization, punctuation, or venue-specific style, but no blocked record receives a BibTeX key in this pass.

## Final Ready-Subset BibTeX Audit

[KORA First Paper Final BibTeX Audit - Ready Subset v0.1](kora-first-paper-final-bibtex-audit-ready-subset-v0-1.md) has been created.

Status:

- Current BibTeX remains preliminary.
- Blocked records remain excluded.
- Ready-subset keys remain stable until venue conversion.
- Final bibliography and claim audit are still pending.

## Preliminary BibTeX Entries

```bibtex
@inproceedings{kwon2023pagedattention,
  author = {Kwon, Woosuk and Li, Zhuohan and Zhuang, Siyuan and Sheng, Ying and Zheng, Lianmin and Yu, Cody Hao and Gonzalez, Joseph E. and Zhang, Hao and Stoica, Ion},
  title = {Efficient Memory Management for Large Language Model Serving with PagedAttention},
  booktitle = {SOSP 2023},
  year = {2023},
  doi = {10.48550/arXiv.2309.06180},
  url = {https://arxiv.org/abs/2309.06180}
}

@inproceedings{lewis2020rag,
  author = {Lewis, Patrick and Perez, Ethan and Piktus, Aleksandra and Petroni, Fabio and Karpukhin, Vladimir and Goyal, Naman and Kuttler, Heinrich and Lewis, Mike and Yih, Wen-tau and Rocktaschel, Tim and Riedel, Sebastian and Kiela, Douwe},
  title = {Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks},
  booktitle = {NeurIPS 2020},
  year = {2020},
  doi = {10.48550/arXiv.2005.11401},
  url = {https://arxiv.org/abs/2005.11401}
}

@article{koster2012snakemake,
  author = {Koster, Johannes and Rahmann, Sven},
  title = {Snakemake-a scalable bioinformatics workflow engine},
  journal = {Bioinformatics},
  volume = {28},
  number = {19},
  pages = {2520--2522},
  year = {2012},
  doi = {10.1093/bioinformatics/bts480},
  url = {https://doi.org/10.1093/bioinformatics/bts480}
}

@inproceedings{yao2023react,
  author = {Yao, Shunyu and Zhao, Jeffrey and Yu, Dian and Du, Nan and Shafran, Izhak and Narasimhan, Karthik and Cao, Yuan},
  title = {ReAct: Synergizing Reasoning and Acting in Language Models},
  booktitle = {ICLR 2023},
  year = {2023},
  doi = {10.48550/arXiv.2210.03629},
  url = {https://arxiv.org/abs/2210.03629}
}

@inproceedings{bang2023gptcache,
  author = {Bang, Fu},
  title = {GPTCache: An Open-Source Semantic Cache for LLM Applications Enabling Faster Answers and Cost Savings},
  booktitle = {Proceedings of the 3rd Workshop for Natural Language Processing Open Source Software},
  pages = {212--218},
  publisher = {Association for Computational Linguistics},
  year = {2023},
  doi = {10.18653/v1/2023.nlposs-1.24},
  url = {https://aclanthology.org/2023.nlposs-1.24/}
}

@inproceedings{jimenez2024swebench,
  author = {Jimenez, Carlos E. and Yang, John and Wettig, Alexander and Yao, Shunyu and Pei, Kexin and Press, Ofir and Narasimhan, Karthik},
  title = {SWE-bench: Can Language Models Resolve Real-World GitHub Issues?},
  booktitle = {ICLR 2024},
  year = {2024},
  doi = {10.48550/arXiv.2310.06770},
  url = {https://arxiv.org/abs/2310.06770}
}

@inproceedings{ribeiro2020checklist,
  author = {Ribeiro, Marco Tulio and Wu, Tongshuang and Guestrin, Carlos and Singh, Sameer},
  title = {Beyond Accuracy: Behavioral Testing of NLP Models with CheckList},
  booktitle = {Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics},
  pages = {4902--4912},
  year = {2020},
  doi = {10.18653/v1/2020.acl-main.442},
  url = {https://aclanthology.org/2020.acl-main.442/}
}
```

## Expanded Preliminary BibTeX Candidate Subset

[KORA First Paper Expanded BibTeX Candidate Audit v0.1](kora-first-paper-expanded-bibtex-candidate-audit-v0-1.md) checked the candidate subset `[R03]`, `[R04]`, `[R05]`, `[R07]`, `[R09]`, `[R10]`, `[R12]`, `[R13]`, and `[R16]`.

All nine candidates pass the final field check for preliminary BibTeX using existing repository metadata. The entries below remain preliminary. They do not complete full BibTeX, do not modify manuscript v0.3, and do not make the paper submission-ready.

No candidate from this subset was excluded by the final field check.

```bibtex
@misc{onnxruntime_docs_accessed2026,
  author = {{ONNX Runtime project / Microsoft}},
  title = {ONNX Runtime},
  howpublished = {ONNX Runtime official documentation},
  url = {https://onnxruntime.ai/docs/},
  note = {Accessed 2026-05-11}
}

@misc{langchain_langgraph_graph_api_accessed2026,
  author = {{LangChain}},
  title = {LangGraph Graph API overview},
  howpublished = {LangGraph official documentation},
  url = {https://docs.langchain.com/oss/python/langgraph/graph-api},
  note = {Accessed 2026-05-11}
}

@misc{khattab2023dspy,
  author = {Khattab, Omar and Singhvi, Arnav and Maheshwari, Paridhi and Zhang, Zhiyuan and Santhanam, Keshav and Vardhamanan, Sri and Haq, Saiful and Sharma, Ashutosh and Joshi, Thomas T. and Moazam, Hanna and Miller, Heather and Zaharia, Matei and Potts, Christopher},
  title = {DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines},
  howpublished = {arXiv:2310.03714},
  year = {2023},
  url = {https://arxiv.org/abs/2310.03714}
}

@misc{apacheairflow_dags_accessed2026,
  author = {{Apache Software Foundation / Apache Airflow project}},
  title = {Dags},
  howpublished = {Apache Airflow 3.2.1 documentation},
  url = {https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html},
  note = {Accessed 2026-05-11}
}

@misc{ggmlorg_llamacpp_accessed2026,
  author = {{ggml-org}},
  title = {llama.cpp: LLM inference in C/C++},
  howpublished = {GitHub repository},
  url = {https://github.com/ggml-org/llama.cpp},
  note = {Accessed 2026-05-11}
}

@misc{acm2020artifactreviewbadging,
  author = {{Association for Computing Machinery}},
  title = {Artifact Review and Badging - Current},
  howpublished = {ACM policy page, Version 1.1},
  year = {2020},
  url = {https://www.acm.org/publications/policies/artifact-review-and-badging-current}
}

@misc{schick2023toolformer,
  author = {Schick, Timo and Dwivedi-Yu, Jane and Dessi, Roberto and Raileanu, Roberta and Lomeli, Maria and Zettlemoyer, Luke and Cancedda, Nicola and Scialom, Thomas},
  title = {Toolformer: Language Models Can Teach Themselves to Use Tools},
  howpublished = {arXiv:2302.04761},
  year = {2023},
  doi = {10.48550/arXiv.2302.04761},
  url = {https://arxiv.org/abs/2302.04761}
}

@misc{gao2022pal,
  author = {Gao, Luyu and Madaan, Aman and Zhou, Shuyan and Alon, Uri and Liu, Pengfei and Yang, Yiming and Callan, Jamie and Neubig, Graham},
  title = {PAL: Program-aided Language Models},
  howpublished = {arXiv:2211.10435},
  year = {2022},
  doi = {10.48550/arXiv.2211.10435},
  url = {https://arxiv.org/abs/2211.10435},
  note = {Revised 2023}
}

@misc{pineau2020reproducibility,
  author = {Pineau, Joelle and Vincent-Lamarre, Philippe and Sinha, Koustuv and Lariviere, Vincent and Beygelzimer, Alina and d'Alche-Buc, Florence and Fox, Emily and Larochelle, Hugo},
  title = {Improving Reproducibility in Machine Learning Research (A Report from the NeurIPS 2019 Reproducibility Program)},
  howpublished = {arXiv:2003.12206},
  year = {2020},
  doi = {10.48550/arXiv.2003.12206},
  url = {https://arxiv.org/abs/2003.12206}
}
```

## Excluded Records

Records still excluded from BibTeX after this expanded candidate pass:

- `[R17]`, `[R18]`: deferred until target-venue selection.
- `[R02]`, `[R15]`, `[R19]`, `[R20]`, `[R22]`, `[R23]`: still not eligible because author-list, split, or venue/style decisions remain unresolved.

No BibTeX is generated for deferred or still-not-eligible records in this document.

## Claim-Safety Note

Preliminary BibTeX does not change claim support.

External references remain related-work, methodology, reproducibility, benchmark-construction, or background support only. KORA's 80/100 result remains supported by KORA deterministic-heavy benchmark docs and evidence. These references do not support production cost reduction proof, real API-cost reduction proof, energy reduction evidence, production benchmark proof, broad workload superiority, or formal artifact approval.

## Next Step

1. Normalize BibTeX keys and field style after the target venue or report format is chosen.
2. Resolve blocked-record metadata and style gaps.
3. Run final bibliography and claim audit.
4. Create manuscript v0.4 only after bibliography and claim audit are stable.
