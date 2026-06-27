# Format-Validation Standards (TRUTH SOURCE — FREEZE BEFORE TEST GENERATION)

This memo is one of three truth sources for the KORA target-workload demo. It
fixes **which library / standard is authoritative** for each format type, the
**exact validation call**, and the **edge cases** that must appear in the test
set. Both sides derive from this memo and nothing else:

- `generate.py` computes each case's **ground truth** by calling the authoritative
  library here (never by hand-labelling).
- `kora/handlers.py` runs the **same** library call to decide valid/invalid.

Because ground truth and the deterministic handler call the *identical* library,
KORA is expected to score ~100% on well-formed format queries **by
construction** — that is the whole point: the deterministic path *is* the
library. The interesting contrast is the LLM trying to reproduce calendar/parsing
rules from parametric knowledge. We do **not** tune anything to individual test
cases (Safety Guard #3).

> FREEZE RULE (Safety Guard #1): once the test set is generated and the blind run
> starts, the library versions, the calls below, and the abstain conditions are
> frozen. Any post-hoc change is forbidden; if truly unavoidable it must be logged
> in `results/RULE_CHANGES.log` with a reason.

---

## 1. Email

- **Authoritative library:** `email-validator` (PyPI `email-validator`).
- **Call:** `email_validator.validate_email(candidate, check_deliverability=False)`.
  - `check_deliverability=False` so we test **syntax/normalization only**, not DNS
    (offline, deterministic, reproducible).
  - Valid ⇔ the call returns without raising; Invalid ⇔ it raises
    `EmailNotValidError`.
- **What counts as valid (per the library, RFC 5321/6531 as it implements):**
  normal `local@domain` addresses, plus-tagging (`a+tag@x.com`), subdomains,
  IDN/Unicode domains that the library normalizes.
- **Edge cases that MUST be represented (≈ half invalid):**
  - missing `@` (`foo.example.com`) → invalid
  - double `@` (`a@@b.com`) → invalid
  - leading/trailing dot in local part (`.a@b.com`, `a.@b.com`) → invalid
  - empty local or domain (`@b.com`, `a@`) → invalid
  - space inside (`a b@c.com`) → invalid
  - domain without TLD / bare hostname (`a@localhost`) → invalid under our call
    (no deliverability, but library still requires a dotted domain)
  - trailing dot in domain (`a@b.com.`) → invalid
  - valid plus-tag (`user+promo@example.com`) → valid
  - valid subdomain (`u@mail.example.co.uk`) → valid

## 2. Phone

- **Authoritative library:** `phonenumbers` (Google libphonenumber port).
- **Default region for parsing:** `"US"`. Numbers may also be given in E.164
  (`+<country><national>`); E.164 parses without a region hint.
- **Call:** `n = phonenumbers.parse(candidate, "US")` then
  `phonenumbers.is_valid_number(n)`.
  - Valid ⇔ parses **and** `is_valid_number` is True.
  - Invalid ⇔ `parse` raises `NumberParseException` **or** `is_valid_number` is
    False. (A string can be *parseable* but not a valid number — both fail here.)
- **Edge cases that MUST be represented:**
  - valid US 10-digit (`(415) 555-2671`) — note: libphonenumber treats `555-01xx`
    as the reserved-but-valid test range; we use real-looking valids the library
    accepts and confirm each at generate time.
  - valid E.164 (`+14155552671`, `+442071838750`)
  - too few digits (`415-555`) → invalid
  - too many digits (`+1 415 555 2671 999`) → invalid
  - invalid area/prefix the library rejects → invalid
  - letters mixed in (`415-555-ABCD`) → invalid (parse raises)
  - empty / punctuation only → invalid
  > Ground truth is whatever `is_valid_number` returns — we never assert a number
  > is valid/invalid by hand; generate.py records the library's verdict.

## 3. Date

- **Authoritative module:** Python standard library `datetime` (real proleptic
  Gregorian calendar).
- **Expected input format:** ISO-like `YYYY-MM-DD`.
- **Call:** `datetime.datetime.strptime(candidate, "%Y-%m-%d")`.
  - Valid ⇔ parses to a real calendar date.
  - Invalid ⇔ raises `ValueError` (bad format **or** non-existent calendar date).
- **Edge cases that MUST be represented:**
  - leap day valid: `2024-02-29` (2024 divisible by 4) → valid
  - leap day invalid: `2023-02-29` → invalid (not a leap year)
  - century non-leap: `1900-02-29` → invalid (÷100, not ÷400)
  - century leap: `2000-02-29` → valid (÷400)
  - month 13 (`2024-13-01`) → invalid
  - day 31 in 30-day month (`2024-04-31`, `2024-06-31`) → invalid
  - day 00 (`2024-05-00`) → invalid
  - wrong separators / non-ISO order (`31/12/2024`, `2024.12.31`) → invalid
    (format mismatch under `%Y-%m-%d`)
  - normal valid date (`2025-07-15`) → valid

---

## Dispatcher routing & ABSTAIN conditions for format queries

The KORA front-door dispatcher only handles a query deterministically when it can
**confidently** identify (a) that it is a single, explicit format-validation
request and (b) the exact candidate string and its type. Otherwise it **abstains**
and the query escalates to the LLM. Abstain conditions (derived from the task's
nature, not from test answers):

- The request does not clearly ask "is this a valid <email|phone|date>?" for one
  specific candidate (e.g. it asks *why* it's invalid, or asks to *fix* it, or
  compares two) → abstain (this is reasoning, not validation).
- The candidate type is ambiguous (e.g. `12345678` could be a phone or an id, or
  the text says "this value" without a type) → abstain.
- More than one candidate is present and the intent is unclear → abstain.
- No extractable candidate token of the declared type → abstain.

These abstain rules are what the **trap** category exercises: inputs that *look*
like format checks but are actually under-specified, so the correct behaviour is
to escalate, not to route.

---

## Library versions (filled in at freeze time by generate.py)

generate.py records the installed versions of `email-validator` and
`phonenumbers` into the results payload so the frozen ground truth is
reproducible. If a library is missing from the `kora-benchmark` venv, install it
there **before** freezing and note the version here.
