# spec/SKILL_CONTRACTS.md

# Skill Contracts — Input / Output Schemas

## Purpose

This document defines **strict contracts** between the MainAgent and each Skill.
If a Skill violates its contract, the output is invalid and must be discarded.

These contracts guarantee:

* Interchangeable Skills
* Predictable pipelines
* Cross-agent and cross-API continuity

---

## Global Contract Rules

### C1. JSON-Serializable Only

* All Skill outputs must be JSON-serializable
* No markdown, no prose blobs

### C2. Explicit Fields Only

* No implicit assumptions
* Missing fields = invalid output

### C3. Deterministic Naming

* Field names must never change
* Versioned changes require explicit migration

---

## 1. ResearchSkill Contract

### Input

```json
{
  "topic": "string",
  "target_audience": "string | null",
  "constraints": "string | null"
}
```

### Output

```json
{
  "audience_pain": ["string"],
  "curiosity_gaps": ["string"],
  "emotional_triggers": ["string"],
  "controversial_angles": ["string"]
}
```

### Notes

* Arrays must contain at least 3 items each
* Generic statements are invalid

---

## 2. ClickThesis Contract (Logical Artifact)

### Definition

A single sentence that explains **why this video must be clicked**.

### Rules

* Exactly one sentence
* Emotionally charged
* Time- or consequence-bound

### Example (valid)

"Most people believe X is safe — this video shows why it quietly destroys Y."

---

## 3. CTRSkill Contract

### Input

```json
{
  "click_thesis": "string",
  "research": {
    "audience_pain": ["string"],
    "curiosity_gaps": ["string"],
    "emotional_triggers": ["string"],
    "controversial_angles": ["string"]
  }
}
```

### Output

```json
{
  "hooks": ["string"],
  "titles": ["string"],
  "thumbnail_texts": ["string"]
}
```

### Constraints

* Each array must contain at least 5 items
* Thumbnail texts must be ≤ 6 words

---

## 4. ScriptSkill Contract

### Input

```json
{
  "selected_hook": "string",
  "selected_title": "string",
  "click_thesis": "string"
}
```

### Output

```json
{
  "script": "string"
}
```

### Constraints

* First 15 seconds must explicitly address ClickThesis
* No cold open allowed

---

## 5. EvalSkill Contract

### Input

```json
{
  "click_thesis": "string",
  "hook": "string",
  "title": "string",
  "thumbnail_text": "string",
  "script": "string"
}
```

### Output

```json
{
  "result": "PASS | FAIL",
  "failure_reason": "string | null",
  "confidence": "float"
}
```

### Rules

* FAIL must always include failure_reason
* confidence range: 0.0 – 1.0

---

## 6. Contract Violation Handling

* Any violation → immediate discard
* No partial acceptance
* Agent must re-run the responsible Skill

---

## 7. Compatibility Guarantee

Any Skill implementation that follows this document:

* Is drop-in replaceable
* Requires no Agent changes

If not, the Skill is invalid.
