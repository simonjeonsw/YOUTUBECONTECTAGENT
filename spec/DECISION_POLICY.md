# spec/DECISION_POLICY.md

# Decision Policy — MainAgent

## Purpose

This document defines **explicit, model-agnostic decision rules** that the MainAgent must follow.
All decisions must be explainable by referencing this policy.

---

## 1. General Rules

### G1. Artifact-First

* Decisions must rely on written artifacts, not prior conversation
* If required context is missing, the Agent must regenerate it

### G2. CTR Priority

* When trade-offs exist, choose the option with higher CTR potential

### G3. Minimal Execution

* Skip Skills if their output will not materially affect CTR

---

## 2. Skill Invocation Rules

### R1. When to Run ResearchSkill

Run if:

* Topic is abstract, technical, or unfamiliar
* Target audience is unclear

Skip if:

* Topic is common knowledge
* User provides clear framing

---

### R2. ClickThesis Validation

* Must be a single sentence
* Must express *why clicking is necessary now*
* Must be emotionally loaded (curiosity, threat, contradiction)

If invalid → regenerate

---

### R3. CTRSkill Execution

* Generate at least:

  * 5 hooks
  * 5 titles
  * 5 thumbnail texts

If fewer than 3 pass Eval pre-check → regenerate

---

### R4. ScriptSkill Execution

* Script must be based on a selected hook + title
* First 10–15 seconds must explicitly resolve ClickThesis promise

---

## 3. Retry Policy

### E1. Eval FAIL Handling

* FAIL due to weak emotion → rerun CTRSkill
* FAIL due to unclear promise → regenerate ClickThesis
* FAIL due to pacing → rerun ScriptSkill

### E2. Retry Limit

* Max retries per Skill: 3
* If still FAIL → surface best available output for human review

---

## 4. Forbidden Actions

* No ad-hoc creative decisions
* No skipping Eval
* No modifying Skill outputs manually

---

## 5. Portability Guarantee

Any new Agent or API must:

* Read this document
* Apply rules exactly
* Produce equivalent decisions

If this cannot be satisfied, the Agent is invalid.
