"""Generate the KORA target-workload test set with ground truth derived ONLY
from the task's nature (libraries / KB / policy functions), never from any model
output or by hand-labelling individual cases (Safety Guard #3).

Case schema (the only fields run.py shows to either arm are `text` and
`payload`; everything else is ground truth / metadata held back to avoid leakage):

    {
      "id":            "fmt-email-001",
      "category":      "format" | "faq" | "policy" | "reasoning" | "trap",
      "subtype":       "email"/"phone"/"date" | <fact_id> | <policy_id> | null,
      "text":          "<user query as sent>",
      "payload":       {<structured fields>} | null,
      "gt_kind":       "valid_invalid" | "kb_answer" | "eligibility" | "freeform",
      "ground_truth":  "valid"/"invalid" | [answer_key...] | "eligible"/"ineligible" | null,
      "should_escalate": bool,     # routing ground truth (ideal: needs the LLM?)
      "meta":          {...}        # candidate / fact_id / canonical answer / looks_like
    }

Run (smoke = ~half of each category):
    ~/kora-ai-champion/envs/kora-benchmark/bin/python \
        experiments/kora_target_workload/generate.py --profile smoke --seed 0
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))  # make the local `kora` package importable

import yaml  # noqa: E402

from kora import format_rules, policy_rules  # noqa: E402

SPEC_DIR = HERE / "spec"
WORKLOAD_DIR = HERE / "workloads"


# --------------------------------------------------------------------------- #
# Profiles (per-category targets; actual counts may be smaller if a pool is
# short — that is logged, never silently padded).
# --------------------------------------------------------------------------- #
PROFILES = {
    "smoke": {"email": 20, "phone": 20, "date": 20,
              "faq_per_fact": 2, "policy_per": 8, "reasoning": 20, "trap": 15},
    "full":  {"email": 40, "phone": 40, "date": 40,
              "faq_per_fact": 4, "policy_per": 16, "reasoning": 40, "trap": 30},
}


# --------------------------------------------------------------------------- #
# 1. FORMAT — curated candidate pools (intent only; the LIBRARY decides the
#    label). We then stratify to ~50:50 valid:invalid by the library's verdict,
#    so a wrong guess about an edge case never skews the balance.
# --------------------------------------------------------------------------- #
EMAIL_POOL = [
    # intended-valid
    "user@example.com", "jane.doe@example.org", "user+promo@example.com",
    "first.last@sub.example.co.uk", "john_doe@example.com", "a.b.c@example.io",
    "contact@northwind-goods.com", "sales@mail.example.net", "r2d2@example.com",
    "hello@example.travel", "customer123@shop.example.com", "q@example.com",
    "a1@example.com", "b2@example.net", "c.d@example.org", "e_f@example.io",
    "g+h@example.com", "ian@mail.example.com", "jkl@example.co", "mno@example.us",
    "pqr@example.biz", "stu@example.info", "alpha.beta@example.com",
    "gamma@sub.example.org", "delta123@example.com", "foxtrot@example.com",
    "hotel@example.com", "india@example.com",
    # intended-invalid (edge cases from format_standards.md)
    "foo.example.com", "a@@b.com", ".leading@example.com", "trailing.@example.com",
    "@nodomain.com", "noatdomain@", "has space@example.com", "user@exam ple.com",
    "user@@@example.com", "plaintext", "user@.com", "user@domain..com",
    "a@localhost", "user@example.com.",
    "abc@", "@def.com", "ghi@", "mno@@pqr.com", "stu vwx@example.com",
    "a@b@c.com", "double..dot@example.com", ".start2@example.com",
    "end2.@example.com", "noatsymbol2.com", "spaces in2@example.com",
    "a@.leadingdot.com", "trailingdot2@domain.com.", "a@b..c.com",
    "weird@@@x.com", "x y z@example.com", "no_tld@example", "()@example.com",
]
PHONE_POOL = [
    # intended-valid (real geographic / E.164)
    "(212) 736-5000", "+1 212 736 5000", "(415) 362-0788", "+14153620788",
    "+44 20 7183 8750", "+61 2 9374 4000", "(202) 456-1111", "+12024561111",
    "(312) 726-7000", "+13127267000", "(305) 358-5900", "(404) 521-5000",
    "+14045215000",
    "(312) 744-5000", "+1 312 744 5000", "(617) 267-9300", "+1 617 267 9300",
    "(206) 684-4000", "+1 206 684 4000", "(702) 731-7110", "+1 702 731 7110",
    "(213) 626-4280", "+1 213 626 4280", "+33 1 42 68 53 00", "+81 3 3201 3331",
    "+44 20 7930 4832", "+61 2 9374 4001", "(305) 461-4000", "(404) 614-2000",
    "+1 305 461 4000", "+1 404 614 2000",
    # intended-invalid
    "415-555", "123", "+1 415 555 2671 999", "555-ABCD", "(000) 000-0000",
    "+1 000 000 0000", "abcdefghij", "+999 99 999", "12", "   ", "+1-23",
    "00000", "1", "+1 1", "(999) 999-99999", "phone", "++1234",
    "+1 555 555 5555 5555", "123-45-6789", "(12) 34", "+0 000", "555.555",
    "+1()", "abc-def-ghij", "9999999999999999", "(415) 000-0000", "+",
]
DATE_POOL = [
    # intended-valid (incl. leap-year edges)
    "2025-01-15", "2024-02-29", "2000-02-29", "2023-07-04", "2020-12-31",
    "1999-06-30", "2024-04-30", "2022-02-28", "2025-11-09", "2021-08-17",
    "2025-03-14", "2025-06-21", "2024-10-31", "2023-11-30", "2022-09-15",
    "2021-01-01", "2019-12-25", "2018-07-04", "2016-02-29", "2012-02-29",
    "2008-02-29", "2026-05-05", "2027-08-19", "2015-03-31", "2017-10-10",
    "2014-06-30",
    # intended-invalid (calendar + format edges)
    "2023-02-29", "1900-02-29", "2024-13-01", "2024-04-31", "2024-06-31",
    "2024-05-00", "2024-00-10", "2024-12-32", "2024-02-30", "31/12/2024",
    "2024.12.31", "Dec-31-2024",
    "2025-02-29", "2100-02-29", "2025-13-15", "2025-04-31", "2025-09-31",
    "2025-11-31", "2025-06-00", "2025-01-32", "2025/03/14", "14-03-2025",
    "March 14 2025", "20250314", "2025-04-00", "0000-00-00", "2025-12-00",
    "2025-00-01",
]

FORMAT_TEMPLATES = {
    "email": "Is this a valid email address: {c}",
    "phone": "Is this a valid phone number: {c}",
    "date": "Is this a valid calendar date in YYYY-MM-DD format: {c}",
}


def build_format_cases(fmt_type: str, pool: list[str], n: int) -> list[dict]:
    """Label every candidate with the authoritative library, then take a
    ~50:50 valid/invalid slice in curated order (edge cases first)."""
    labeled = [(c, format_rules.validate(fmt_type, c)) for c in pool]
    valids = [c for c, lab in labeled if lab == format_rules.VALID]
    invalids = [c for c, lab in labeled if lab == format_rules.INVALID]

    half_v = min(n // 2, len(valids))
    half_i = min(n - half_v, len(invalids))
    # if one side is short, backfill from the other to hit n where possible
    if half_v + half_i < n:
        half_v = min(n - half_i, len(valids))
    chosen = [(c, format_rules.VALID) for c in valids[:half_v]] + \
             [(c, format_rules.INVALID) for c in invalids[:half_i]]

    cases = []
    for i, (cand, label) in enumerate(chosen, start=1):
        cases.append({
            "id": f"fmt-{fmt_type}-{i:03d}",
            "category": "format",
            "subtype": fmt_type,
            "text": FORMAT_TEMPLATES[fmt_type].format(c=cand),
            "payload": None,
            "gt_kind": "valid_invalid",
            "ground_truth": label,
            "should_escalate": False,
            "meta": {"candidate": cand},
        })
    return cases, {"valid": half_v, "invalid": half_i, "pool": len(pool)}


# --------------------------------------------------------------------------- #
# 2. FAQ — paraphrases (genuine linguistic variation authored from the
#    canonical question's MEANING; ground truth = the fact's frozen answer_key).
# --------------------------------------------------------------------------- #
PARAPHRASES = {
    "weekday_hours": [
        "When are you open during the week?",
        "What time do your stores open on weekdays?",
        "I want to visit on a Wednesday — what are your weekday hours?",
        "Until when are you open Monday through Friday?",
    ],
    "weekend_hours": [
        "Are you open on Saturdays, and until when?",
        "What are your hours over the weekend?",
        "Can I come by on a Saturday or Sunday?",
        "What time do you close on the weekend?",
    ],
    "refund_window": [
        "How many days do I have to ask for a refund?",
        "What's the time limit on getting my money back?",
        "Is there a deadline to return something for a refund?",
        "How long after delivery can I still request a refund?",
    ],
    "shipping_fee": [
        "How much do you charge for shipping?",
        "What's the delivery cost on an order?",
        "Do I have to pay a shipping fee, and how much?",
        "Is there a postage charge, or is delivery free?",
    ],
    "shipping_time_domestic": [
        "How many days until my domestic order arrives?",
        "How fast is delivery within the country?",
        "When will my order ship and get here domestically?",
        "How long does standard local delivery take?",
    ],
    "shipping_time_international": [
        "How long does shipping abroad take?",
        "When will an overseas order arrive?",
        "What's the delivery time for international orders?",
        "How many days to ship internationally?",
    ],
    "support_email": [
        "What email address can I use to contact support?",
        "Where do I email if I need help?",
        "What is your customer support e-mail address?",
        "Is there a support email I can reach you at?",
    ],
    "support_phone": [
        "What number do I call for support?",
        "How can I phone customer service?",
        "Is there a support telephone number I can call?",
        "What's the phone number to reach your help line?",
    ],
    "payment_methods": [
        "Which cards do you take at checkout?",
        "What ways can I pay for my order?",
        "What payment methods do you accept?",
        "How can I pay — do you accept PayPal?",
    ],
    "warranty_period": [
        "How long is the warranty on electronics?",
        "What's the guarantee length on electronic items?",
        "How many months are electronics covered for?",
        "Do electronics come with a warranty, and for how long?",
    ],
    "loyalty_program": [
        "How do I earn rewards points?",
        "Can you explain how your loyalty points program works?",
        "How many points do I get and what are they worth?",
        "How does earning and redeeming rewards work?",
    ],
    "password_reset": [
        "How can I reset my password?",
        "I forgot my password — how do I change it?",
        "Where do I go to reset my account password?",
        "How do I recover access when I can't log in with my password?",
    ],
    "order_tracking": [
        "How do I track my order?",
        "Where can I see my shipment's tracking status?",
        "How can I follow where my package is?",
        "Where do I find tracking for my order?",
    ],
    "gift_card_expiry": [
        "Do your gift cards expire?",
        "Is there an expiration date on gift cards?",
        "How long is a gift card valid for?",
        "Will my gift card ever run out?",
    ],
    "return_address": [
        "Where should I mail my returns?",
        "What address do I send returned items to?",
        "Where do returns need to be shipped?",
        "What is the return shipping address?",
    ],
}


def build_faq_cases(facts: list[dict], per_fact: int) -> list[dict]:
    cases = []
    idx = 1
    for fact in facts:
        fid = fact["id"]
        paras = PARAPHRASES.get(fid, [])[:per_fact]
        for para in paras:
            cases.append({
                "id": f"faq-{idx:03d}",
                "category": "faq",
                "subtype": fid,
                "text": para,
                "payload": None,
                "gt_kind": "kb_answer",
                "ground_truth": [k.lower() for k in fact["answer_key"]],
                "should_escalate": False,
                "meta": {"fact_id": fid, "canonical_answer": fact["answer"]},
            })
            idx += 1
    return cases


# --------------------------------------------------------------------------- #
# 3. POLICY — structured inputs incl. boundary values; GT via the reference
#    evaluator (policy_rules.evaluate), never hand-set.
# --------------------------------------------------------------------------- #
POLICY_TEXT = {
    "refund_eligibility": "Determine refund eligibility for this order.",
    "free_shipping": "Determine whether this order qualifies for free shipping.",
    "welcome_coupon": "Determine whether the WELCOME10 coupon is valid here.",
    "warranty_claim": "Determine whether this warranty claim is covered.",
    "return_label": "Determine free prepaid return-label eligibility.",
}

POLICY_PAYLOADS = {
    "refund_eligibility": [
        {"days_since_delivery": 10, "item_category": "books", "opened": True},
        {"days_since_delivery": 30, "item_category": "clothing", "opened": False},
        {"days_since_delivery": 31, "item_category": "clothing", "opened": False},
        {"days_since_delivery": 5, "item_category": "electronics", "opened": False},
        {"days_since_delivery": 5, "item_category": "electronics", "opened": True},
        {"days_since_delivery": 2, "item_category": "food", "opened": False},
        {"days_since_delivery": 45, "item_category": "books", "opened": False},
        {"days_since_delivery": 0, "item_category": "other", "opened": True},
        {"days_since_delivery": 20, "item_category": "clothing", "opened": True},
        {"days_since_delivery": 29, "item_category": "electronics", "opened": False},
        {"days_since_delivery": 30, "item_category": "electronics", "opened": False},
        {"days_since_delivery": 31, "item_category": "electronics", "opened": False},
        {"days_since_delivery": 0, "item_category": "food", "opened": True},
        {"days_since_delivery": 15, "item_category": "other", "opened": False},
        {"days_since_delivery": 30, "item_category": "books", "opened": True},
        {"days_since_delivery": 31, "item_category": "food", "opened": False},
    ],
    "free_shipping": [
        {"order_total": 60, "destination_zone": "domestic", "membership": "none"},
        {"order_total": 50, "destination_zone": "domestic", "membership": "none"},
        {"order_total": 49.99, "destination_zone": "domestic", "membership": "none"},
        {"order_total": 200, "destination_zone": "international", "membership": "plus"},
        {"order_total": 10, "destination_zone": "remote", "membership": "plus"},
        {"order_total": 80, "destination_zone": "remote", "membership": "none"},
        {"order_total": 5, "destination_zone": "domestic", "membership": "plus"},
        {"order_total": 49.99, "destination_zone": "international", "membership": "none"},
        {"order_total": 100, "destination_zone": "domestic", "membership": "none"},
        {"order_total": 50.0, "destination_zone": "remote", "membership": "none"},
        {"order_total": 50, "destination_zone": "remote", "membership": "plus"},
        {"order_total": 49.99, "destination_zone": "domestic", "membership": "plus"},
        {"order_total": 0, "destination_zone": "domestic", "membership": "plus"},
        {"order_total": 1000, "destination_zone": "international", "membership": "none"},
        {"order_total": 75, "destination_zone": "domestic", "membership": "none"},
        {"order_total": 25, "destination_zone": "domestic", "membership": "none"},
    ],
    "welcome_coupon": [
        {"account_age_days": 3, "prior_orders": 0, "coupon_code": "WELCOME10"},
        {"account_age_days": 14, "prior_orders": 0, "coupon_code": "WELCOME10"},
        {"account_age_days": 15, "prior_orders": 0, "coupon_code": "WELCOME10"},
        {"account_age_days": 5, "prior_orders": 1, "coupon_code": "WELCOME10"},
        {"account_age_days": 5, "prior_orders": 0, "coupon_code": "SAVE20"},
        {"account_age_days": 0, "prior_orders": 0, "coupon_code": "WELCOME10"},
        {"account_age_days": 30, "prior_orders": 2, "coupon_code": "WELCOME10"},
        {"account_age_days": 1, "prior_orders": 0, "coupon_code": "welcome10"},
        {"account_age_days": 7, "prior_orders": 0, "coupon_code": "WELCOME10"},
        {"account_age_days": 13, "prior_orders": 0, "coupon_code": "WELCOME10"},
        {"account_age_days": 14, "prior_orders": 1, "coupon_code": "WELCOME10"},
        {"account_age_days": 20, "prior_orders": 0, "coupon_code": "WELCOME10"},
        {"account_age_days": 0, "prior_orders": 5, "coupon_code": "WELCOME10"},
        {"account_age_days": 10, "prior_orders": 0, "coupon_code": "WELCOME20"},
        {"account_age_days": 9, "prior_orders": 0, "coupon_code": "WELCOME10"},
        {"account_age_days": 14, "prior_orders": 0, "coupon_code": "WELCOME11"},
    ],
    "warranty_claim": [
        {"months_since_purchase": 6, "product_category": "electronics", "defect_type": "manufacturing"},
        {"months_since_purchase": 12, "product_category": "electronics", "defect_type": "manufacturing"},
        {"months_since_purchase": 13, "product_category": "electronics", "defect_type": "manufacturing"},
        {"months_since_purchase": 24, "product_category": "appliance", "defect_type": "manufacturing"},
        {"months_since_purchase": 25, "product_category": "appliance", "defect_type": "manufacturing"},
        {"months_since_purchase": 6, "product_category": "accessory", "defect_type": "manufacturing"},
        {"months_since_purchase": 3, "product_category": "electronics", "defect_type": "accidental"},
        {"months_since_purchase": 2, "product_category": "accessory", "defect_type": "wear"},
        {"months_since_purchase": 11, "product_category": "electronics", "defect_type": "manufacturing"},
        {"months_since_purchase": 12, "product_category": "electronics", "defect_type": "accidental"},
        {"months_since_purchase": 1, "product_category": "appliance", "defect_type": "manufacturing"},
        {"months_since_purchase": 24, "product_category": "appliance", "defect_type": "wear"},
        {"months_since_purchase": 7, "product_category": "accessory", "defect_type": "manufacturing"},
        {"months_since_purchase": 5, "product_category": "accessory", "defect_type": "manufacturing"},
        {"months_since_purchase": 13, "product_category": "appliance", "defect_type": "manufacturing"},
        {"months_since_purchase": 0, "product_category": "electronics", "defect_type": "manufacturing"},
    ],
    "return_label": [
        {"reason": "defective", "days_since_delivery": 10},
        {"reason": "defective", "days_since_delivery": 30},
        {"reason": "defective", "days_since_delivery": 31},
        {"reason": "wrong_item", "days_since_delivery": 5},
        {"reason": "changed_mind", "days_since_delivery": 5},
        {"reason": "changed_mind", "days_since_delivery": 31},
        {"reason": "wrong_item", "days_since_delivery": 31},
        {"reason": "defective", "days_since_delivery": 0},
        {"reason": "defective", "days_since_delivery": 20},
        {"reason": "wrong_item", "days_since_delivery": 30},
        {"reason": "wrong_item", "days_since_delivery": 31},
        {"reason": "changed_mind", "days_since_delivery": 0},
        {"reason": "changed_mind", "days_since_delivery": 30},
        {"reason": "defective", "days_since_delivery": 29},
        {"reason": "wrong_item", "days_since_delivery": 15},
        {"reason": "changed_mind", "days_since_delivery": 31},
    ],
}


def build_policy_cases(per_policy: int) -> list[dict]:
    cases = []
    idx = 1
    for policy_id, payloads in POLICY_PAYLOADS.items():
        for payload in payloads[:per_policy]:
            gt = policy_rules.evaluate(policy_id, payload)
            cases.append({
                "id": f"pol-{idx:03d}",
                "category": "policy",
                "subtype": policy_id,
                "text": POLICY_TEXT[policy_id],
                "payload": payload,
                "gt_kind": "eligibility",
                "ground_truth": gt,
                "should_escalate": False,
                "meta": {"policy_id": policy_id},
            })
            idx += 1
    return cases


# --------------------------------------------------------------------------- #
# 4. REASONING — free-form ambiguous queries that MUST escalate (no
#    deterministic ground truth; routing GT = should_escalate True).
# --------------------------------------------------------------------------- #
REASONING = [
    "My package arrived but the box was crushed and one item is missing. What should I do?",
    "I'm deciding between the Plus membership and paying shipping each time. I order about twice a month — which is better for me?",
    "The product I received doesn't look like the photos on your website. Is that something you can help with?",
    "Can you help me figure out why my coupon was rejected at checkout yesterday?",
    "I just moved and I'm worried my order is going to my old address. What are my options?",
    "Is it worth upgrading the warranty on a blender I use every single day?",
    "I had a rude interaction with a delivery driver. Who can I talk to about that?",
    "What's the smartest way to return several items that came from different orders?",
    "I'm not sure whether to return this jacket or exchange it for a different size. What do you recommend?",
    "My order has been 'in transit' for two weeks and I'm getting nervous. Any thoughts?",
    "I bought a gift but the recipient already has one. What's the best path forward?",
    "Would the laptop or the tablet be a better fit for a college student on a budget?",
    "I keep getting charged twice some months and I can't tell why. Can you look into the pattern?",
    "Should I wait for a sale or just buy the headphones now before they sell out?",
    "The assembly instructions are confusing and I'm stuck halfway. Any guidance?",
    "I want to cancel part of my order but keep the rest — is that complicated?",
    "My elderly father struggles with your website. Is there an easier way for him to order?",
    "I'm allergic to certain materials. How do I know which products are safe for me?",
    "The color looked different in person and I'm disappointed. What would you suggest?",
    "I think a competitor has a better deal. Is there anything you can do for me?",
    "I'm planning a big event and need a lot of items by a specific date. How should I approach this?",
    "My account seems to have someone else's order history mixed in. That's concerning — what now?",
    "The whole return process feels overwhelming to me. Can you walk me through my situation?",
    "Would you recommend the extended protection plan for something I rarely use?",
    "My order shows delivered but I never received it. How do we sort this out?",
    "I need to send the same item to three different addresses for the holidays — what's the easiest way?",
    "The size chart confused me and I think I ordered wrong. What should I do now?",
    "I'm worried about the environmental impact of returns. Is there a greener option for me?",
    "Two items in my cart say different delivery dates and I need them together — thoughts?",
    "I got a damaged item as a gift but I don't have the order number. Can you still help?",
    "Is the premium model actually worth the extra cost for someone like me?",
    "My promo didn't stack with the sale and I'm confused about which discount applied.",
    "I keep going back and forth on whether to buy now or wait for Black Friday. Advice?",
    "The reviews are mixed on this product and I can't decide. What would you do?",
    "I think my shipment is stuck at customs. What are my realistic options here?",
    "My grandmother wants to order but doesn't have email. How can she still buy?",
    "I'm not sure if this accessory is compatible with the model I already own.",
    "I was double-billed during a checkout error and I'm anxious about the refund timing.",
    "Should I consolidate my orders or ship them separately to get them faster?",
    "I'm buying for a team of twelve and budgets vary — how should I structure the order?",
    "My card was declined but the funds left my account. What's going on and what do I do?",
]


def build_reasoning_cases(n: int) -> list[dict]:
    cases = []
    for i, text in enumerate(REASONING[:n], start=1):
        cases.append({
            "id": f"rea-{i:03d}",
            "category": "reasoning",
            "subtype": None,
            "text": text,
            "payload": None,
            "gt_kind": "freeform",
            "ground_truth": None,
            "should_escalate": True,
            "meta": {},
        })
    return cases


# --------------------------------------------------------------------------- #
# 5. TRAP — look like format/faq/policy but are under-specified/ambiguous, so
#    the correct behaviour is to ABSTAIN -> escalate (should_escalate True).
#    These test that the dispatcher does NOT over-route.
# --------------------------------------------------------------------------- #
TRAPS = [
    # format-shaped traps
    {"text": "Why is admin@@corp.com not a valid email?", "payload": None, "looks_like": "format/email"},
    {"text": "Can you fix this email for me: john doe@gmail,com", "payload": None, "looks_like": "format/email"},
    {"text": "Is 12345678 a valid number?", "payload": None, "looks_like": "format/phone"},
    {"text": "Is next Monday a valid date for delivery?", "payload": None, "looks_like": "format/date"},
    {"text": "Are these the same person: bob@x.com and Bob@X.com?", "payload": None, "looks_like": "format/email"},
    {"text": "Is +44 7911 123456 a valid US phone number?", "payload": None, "looks_like": "format/phone"},
    {"text": "Which date is earlier, 03-04-2024 or 04-03-2024?", "payload": None, "looks_like": "format/date"},
    # faq-shaped traps (ambiguous between two facts, or not a single KB fact)
    {"text": "What are your hours?", "payload": None, "looks_like": "faq/hours"},
    {"text": "How long does delivery take?", "payload": None, "looks_like": "faq/shipping_time"},
    {"text": "How do I contact you?", "payload": None, "looks_like": "faq/support"},
    {"text": "Do you offer free returns?", "payload": None, "looks_like": "faq/unknown"},
    {"text": "What's your policy on opened electronics?", "payload": None, "looks_like": "faq/refund"},
    # policy-shaped traps (missing field / bad enum / bad type / wrong policy)
    {"text": "Determine refund eligibility for this order.",
     "payload": {"days_since_delivery": 10, "opened": False}, "looks_like": "policy/refund"},
    {"text": "Am I eligible for free shipping?", "payload": None, "looks_like": "policy/free_shipping"},
    {"text": "Is this refundable?",
     "payload": {"days_since_delivery": 12, "item_category": "furniture", "opened": False},
     "looks_like": "policy/refund"},
    {"text": "Determine warranty coverage.",
     "payload": {"months_since_purchase": 5, "product_category": "electronics"},
     "looks_like": "policy/warranty"},
    {"text": "Can I use a coupon?",
     "payload": {"account_age_days": 5, "prior_orders": 0}, "looks_like": "policy/coupon"},
    {"text": "Determine return-label eligibility.",
     "payload": {"reason": "gift", "days_since_delivery": 5}, "looks_like": "policy/return_label"},
    {"text": "Is my order eligible?", "payload": {"days_since_delivery": 20}, "looks_like": "policy/ambiguous"},
    {"text": "Determine free shipping.",
     "payload": {"order_total": "a lot", "destination_zone": "domestic", "membership": "none"},
     "looks_like": "policy/free_shipping"},
    # more format-shaped traps
    {"text": "Should admin@@corp.com be accepted by our signup form?", "payload": None, "looks_like": "format/email"},
    {"text": "Between 2024-02-29 and 2023-02-29, which one is the real date?", "payload": None, "looks_like": "format/date"},
    {"text": "Is 867-5309 enough digits to be a real phone number?", "payload": None, "looks_like": "format/phone"},
    # more faq-shaped traps (ambiguous between facts / not in KB)
    {"text": "When can I reach you?", "payload": None, "looks_like": "faq/hours-or-support"},
    {"text": "How much will my order cost in total?", "payload": None, "looks_like": "faq/shipping_fee"},
    {"text": "What's your policy?", "payload": None, "looks_like": "faq/unknown"},
    {"text": "Can I get a discount?", "payload": None, "looks_like": "faq/unknown"},
    # more policy-shaped traps (missing field / bad enum / no payload / ambiguous)
    {"text": "Determine warranty coverage.",
     "payload": {"product_category": "electronics", "defect_type": "manufacturing"},
     "looks_like": "policy/warranty"},
    {"text": "Is this order eligible for free shipping?",
     "payload": {"order_total": 60, "membership": "none"}, "looks_like": "policy/free_shipping"},
    {"text": "Determine refund eligibility.",
     "payload": {"days_since_delivery": -5, "item_category": "books", "opened": False},
     "looks_like": "policy/refund"},
]


def build_trap_cases(n: int) -> list[dict]:
    cases = []
    for i, t in enumerate(TRAPS[:n], start=1):
        cases.append({
            "id": f"trp-{i:03d}",
            "category": "trap",
            "subtype": None,
            "text": t["text"],
            "payload": t["payload"],
            "gt_kind": "freeform",
            "ground_truth": None,
            "should_escalate": True,
            "meta": {"looks_like": t["looks_like"]},
        })
    return cases


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(description="Generate KORA target workload.")
    parser.add_argument("--profile", choices=list(PROFILES), default="smoke")
    parser.add_argument("--seed", type=int, default=0,
                        help="reserved; generation is deterministic (no sampling)")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    cfg = PROFILES[args.profile]
    kb = yaml.safe_load((SPEC_DIR / "kb.yaml").read_text(encoding="utf-8"))
    facts = kb["facts"]

    cases: list[dict] = []
    fmt_balance = {}
    for fmt_type, pool in (("email", EMAIL_POOL), ("phone", PHONE_POOL), ("date", DATE_POOL)):
        fcases, bal = build_format_cases(fmt_type, pool, cfg[fmt_type])
        cases.extend(fcases)
        fmt_balance[fmt_type] = bal

    cases.extend(build_faq_cases(facts, cfg["faq_per_fact"]))
    cases.extend(build_policy_cases(cfg["policy_per"]))
    cases.extend(build_reasoning_cases(cfg["reasoning"]))
    cases.extend(build_trap_cases(cfg["trap"]))

    counts = {}
    for c in cases:
        counts[c["category"]] = counts.get(c["category"], 0) + 1
    counts["total"] = len(cases)

    payload = {
        "profile": args.profile,
        "seed": args.seed,
        "generated_with": format_rules.lib_versions(),
        "counts": counts,
        "format_balance": fmt_balance,
        "cases": cases,
    }

    out_path = Path(args.out) if args.out else WORKLOAD_DIR / f"{args.profile}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"profile={args.profile}  libs={payload['generated_with']}")
    print(f"counts={counts}")
    print(f"format balance (valid/invalid): {fmt_balance}")
    # quick GT sanity: distribution of ground truth per scorable category
    fmt_gt = {"valid": 0, "invalid": 0}
    pol_gt = {"eligible": 0, "ineligible": 0}
    for c in cases:
        if c["category"] == "format":
            fmt_gt[c["ground_truth"]] += 1
        elif c["category"] == "policy":
            pol_gt[c["ground_truth"]] += 1
    print(f"format GT: {fmt_gt}   policy GT: {pol_gt}")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
