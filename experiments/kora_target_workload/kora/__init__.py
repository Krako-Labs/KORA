"""KORA deterministic core for the target-workload demo.

Shared, single-source-of-truth modules:
  - format_rules : library-backed validators (email/phone/date)
  - policy_rules : structured-input policy evaluators

Both are imported by generate.py (to compute ground truth) AND by the dispatcher
(to answer deterministically), so the two can never diverge. Routing / abstain
logic lives in the dispatcher (added in a later step), not here.
"""
