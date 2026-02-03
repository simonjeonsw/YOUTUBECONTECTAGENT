# /spec/EVAL_POLICY.md

# EVALUATION POLICY — Content Quality Control

## 1. Purpose

This policy defines how generated content is evaluated and filtered
before being accepted as a valid output.

The goal is not to find the "best" content,
but to eliminate content that is unlikely to perform.

Evaluation favors **predictable performance signals**
over subjective creativity.

---

## 2. Evaluation Scope

This policy applies to:

- Hooks (opening sentences)
- Video titles
- Thumbnail text

Each content type is evaluated independently.

---

## 3. Core Evaluation Principles

All evaluated content must satisfy at least one of the following:

- Create emotional tension
- Imply hidden information
- Suggest risk, mistake, or opportunity
- Trigger curiosity through contrast or conflict

Neutral or informational-only content is rejected.

---

## 4. Hook Evaluation Rules

A hook is considered valid if ALL conditions are met:

- Minimum length: 6 words
- Contains at least one emotional or tension-related keyword
- Includes a curiosity trigger:
  - Contrast ("but", "however")
  - Question ("why", "how", implicit uncertainty)

Invalid hook examples:
- Pure statements
- Greetings
- Definitions
- Overly short phrases

---

## 5. Title Evaluation Rules

A title is considered valid if ALL conditions are met:

- Maximum length: 70 characters
- Contains emotional or curiosity-driven language
- Avoids generic framing without tension

Additional rules:
- If the word "about" is used, a curiosity modifier must exist
- Informational titles without emotional implication are rejected

---

## 6. Thumbnail Text Evaluation Rules

Thumbnail text must:

- Be 4 words or fewer
- Contain emotional or tension-inducing language
- Be readable and direct

Long explanations or neutral descriptors are invalid.

---

## 7. Emotional Signal Definition

Emotional signals include (but are not limited to):

- Fear
- Risk
- Mistake
- Curiosity
- Hidden knowledge
- Urgency
- Loss or damage

Exact keywords may evolve, but intent must remain.

---

## 8. Filtering Philosophy

The evaluator is intentionally strict.

It is preferable to:
- Reject many candidates
- Keep only a few high-signal outputs

Quantity can be regenerated.
Low-quality signals should not pass through.

---

## 9. Relationship to Code

This policy is the source of truth.
Evaluation code must implement this policy,
not redefine it.

If a mismatch occurs:
- The policy wins
- The code must be updated

---

## 10. Evolution Policy

Evaluation rules may evolve gradually,
but must remain:

- Deterministic
- Explainable
- Performance-oriented

Any update must be reflected both here
and in the evaluator skill implementation.

