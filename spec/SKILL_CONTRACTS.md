# /spec/SKILL_CONTRACTS.md

# Skill Contracts — Input / Output Schemas

## Purpose

This document defines **strict, version-stable contracts**
between the MainAgent and each Skill.

If a Skill violates its contract, the output is invalid
and must be discarded without partial acceptance.

These contracts guarantee:

- Interchangeable Skills
- Predictable execution pipelines
- Cross-agent and cross-API continuity
- Long-term architectural stability

---

## Global Contract Rules

### C1. JSON-Serializable Only

- All Skill outputs must be JSON-serializable
- No markdown
- No free-form prose blobs
- No hidden metadata

---

### C2. Explicit Fields Only

- All expected fields must be present
- Missing fields = invalid output
- Optional fields must be explicitly defined as optional

---

### C3. Deterministic Naming

- Field names must never change implicitly
- Renaming requires explicit versioning
- Backward compatibility must be preserved

---

### C4. Responsibility Isolation

- Each Skill owns exactly one responsibility
- No Skill may override another Skill’s decision
- Evaluation Skills may filter, but never generate content

---

## 1. ResearchSkill Contract

### Input

```json
{
  "topic": "string",
  "target_audience": "string | null",
  "constraints": "string | null"
}
Output
{
  "audience_pain": ["string"],
  "curiosity_gaps": ["string"],
  "emotional_triggers": ["string"],
  "controversial_angles": ["string"]
}
Rules
Each array must contain at least 3 items

Generic or vague statements are invalid

Research output is signal generation, not conclusions

2. ClickThesis (Logical Artifact)
Definition
A single sentence explaining why the viewer must click this video.

This is not a title.
This is not a hook.
This is the core persuasion logic.

Rules
Exactly one sentence

Emotionally charged

Implies consequence, risk, or hidden outcome

Must be time- or impact-bound

Example (Valid)
"Most people believe X is harmless — this video shows why it quietly destroys Y."

3. CTRSkill Contract
Input
{
  "click_thesis": "string",
  "research": {
    "audience_pain": ["string"],
    "curiosity_gaps": ["string"],
    "emotional_triggers": ["string"],
    "controversial_angles": ["string"]
  },
  "viewer_intent": {
    "intent_tags": ["string"],
    "risk_level": "low | medium | high",
    "curiosity_type": "explicit | implicit | none"
  } | null
}
Output
{
  "hooks": ["string"],
  "titles": ["string"],
  "thumbnail_texts": ["string"]
}
Constraints
Each array must contain at least 5 items

Thumbnail texts must be ≤ 6 words

viewer_intent is optional

CTRSkill must remain functional without viewer_intent

4. ScriptSkill Contract
Input
{
  "selected_hook": "string",
  "selected_title": "string",
  "click_thesis": "string"
}
Output
{
  "script": "string"
}
Rules
The first 15 seconds must explicitly address the ClickThesis

No cold open

No unrelated storytelling before value framing

5. EvalSkill Contract
Input
{
  "click_thesis": "string",
  "hook": "string",
  "title": "string",
  "thumbnail_text": "string",
  "script": "string"
}
Output
{
  "result": "PASS | FAIL",
  "failure_reason": "string | null",
  "confidence": "float"
}
Rules
FAIL must always include failure_reason

PASS must set failure_reason to null

confidence range: 0.0 – 1.0

EvalSkill may only evaluate, never modify content

6. ViewerIntent Skill Contract (Minimal / Optional)
Purpose
ViewerIntent provides lightweight perspective hints
about how content may be perceived by a first-time viewer.

It does NOT make decisions.
It does NOT filter outputs.
It does NOT personalize.

Input
{
  "topic": "string",
  "hook": "string",
  "title": "string"
}
Output
{
  "intent_tags": ["string"],
  "risk_level": "low | medium | high",
  "curiosity_type": "explicit | implicit | none"
}
Rules
Deterministic and rule-based only

No user data

No probabilistic prediction

Output must be safe to ignore by downstream skills

Evolution Note
This Skill may later evolve into:

Persona modeling

Recommendation alignment

Retention optimization

Such evolution must extend this contract,
not break it.

7. Contract Violation Handling
Any contract violation → immediate discard

No partial acceptance

The MainAgent must re-run the responsible Skill only

8. Compatibility Guarantee
Any Skill implementation that follows this document:

Is drop-in replaceable

Requires no MainAgent changes

Is compatible across model and API upgrades

Any Skill that violates this contract is invalid.

## 7. ViewerIntent Skill Contract (Anchor Only)

### Purpose

Defines a **viewer perspective label space** that may be used
by future ranking, evaluation, or personalization systems.

This skill does NOT infer real user behavior.
It only exposes a placeholder intent classification.

---

### Input

```json
{
  "hook": "string",
  "title": "string",
  "thumbnail_text": "string"
}
Output
{
  "viewer_intent": "string | null"
}
Allowed Intent Labels
curiosity_driven
risk_aware
fear_avoidance
status_seeking
time_saver
unknown
Rules
Phase1 implementations must always return "unknown"

No inference logic allowed

No downstream decision may depend on this field

Evolution Policy
Phase2: Soft heuristics allowed

Phase3: Data-driven classification

Phase4: Personalized intent modeling