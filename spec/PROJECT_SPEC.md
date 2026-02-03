# spec/PROJECT_SPEC.md

# PROJECT SPEC — Single Agent, Multi-Skill CTR System

## 0. One-line Definition

A system that **maximizes YouTube CTR and views** by letting a **single decision-making Agent** orchestrate multiple **stateless Skills** (research, CTR, scripting, evaluation) with automatic rejection and rewriting of low-quality outputs.

---

## 1. What This System DOES

* Plans content primarily for **CTR and retention**, not completeness
* Uses **one Agent** to make decisions and control flow
* Executes work through **multiple independent Skills**
* Automatically **evaluates and discards** weak results
* Requires humans only for **final approval**, not iteration

---

## 2. What This System Does NOT Do

* Does NOT rely on multi-agent collaboration by default
* Does NOT give trend data final decision authority
* Does NOT require databases, MCP, or automation to function
* Does NOT optimize for elegance, accuracy, or novelty over views

---

## 3. Core Design Principles (Non-negotiable)

### P1. Agent Thinks, Skills Work

* Agent: planning, sequencing, judging
* Skills: execution only
* Agent never writes content directly

### P2. Skills Are Stateless

* Input → Output only
* No memory, no side effects
* Replaceable without system changes

### P3. Evaluation Is Mandatory

* Every output must pass Eval
* Failed outputs are discarded
* Rewriting loops are expected

### P4. CTR Is the Primary Metric

* If it does not improve CTR, it is not a feature
* Visual clarity > information density

### P5. Decisions Are Policy-Driven (NEW)

* Agent decisions must follow explicit written policies
* No hidden reasoning or ad-hoc judgment
* Policies are model-agnostic and portable

### P6. Continuity Over Sessions (NEW)

* The system must reconstruct context from artifacts, not memory
* No dependency on model-specific hidden state

---

## 4. High-Level Architecture

```
[User Goal]
   ↓
[MainAgent]
   ↓ applies DecisionPolicy
[ResearchSkill]
   ↓
[ClickThesis]  ← single-sentence reason to click (NEW)
   ↓
[CTRSkill]
   ↓
[ScriptSkill]
   ↓
[EvalSkill]
   ↓ PASS / FAIL
[Approved Output]
```

```
[User Goal]
   ↓
[MainAgent]
   ↓ decides
[Skill Pipeline]
   ├─ ResearchSkill
   ├─ CTRSkill
   ├─ ScriptSkill
   └─ EvalSkill
   ↓
[Approved Output]
```

---

## 5. Agent Responsibilities

### MainAgent

**Responsibilities**

* Interpret user intent and constraints
* Apply DecisionPolicy and RetryPolicy
* Generate and validate ClickThesis
* Decide skill execution order
* Judge Eval results and retry if needed

**Explicitly Forbidden**

* Writing scripts
* Generating hooks or titles
* Performing research

---

## 6. Skill Definitions (v1)

### ResearchSkill

* Understand topic and audience
* Extract emotional triggers and conflicts
* Identify curiosity gaps
* Output structured research artifacts

### ClickThesis (Logical Step, Not a Skill)

* Single sentence explaining *why this video must be clicked*
* Serves as the anchor for all downstream outputs
* Used as a hard constraint in CTR, Script, and Eval

### CTRSkill (Critical)

* Generate multiple hooks
* Generate title candidates
* Generate thumbnail text candidates

> System success depends primarily on this Skill

### ScriptSkill

* Write scripts based on selected hook/title
* Optimize first 10–15 seconds for retention

### EvalSkill

* Judge CTR potential
* Detect early-drop risks
* Return PASS / FAIL with reasons

---

## 7. Evaluation Criteria (Summary)

### PASS Conditions

* Hook creates curiosity, threat, or contradiction
* Thumbnail text ≤ 6 words
* Title and thumbnail are not redundant
* Viewer motivation is clear within 10 seconds

### FAIL Conditions

* Explanatory tone
* Pure information listing
* Weak or neutral emotion

---

## 8. Planned Extensions (Explicitly Optional)

### LATER-1: TrendScoutSkill

* Provides weak signals only
* Never overrides Agent judgment

### LATER-2: Memory / Database

* Stores *artifacts*, not thoughts
* Used only to reconstruct past context

### LATER-3: Automation & A/B Testing

* Thumbnail text A/B experiments
* Upload automation

---

## 9. Success Definition

* Produces usable outputs without human iteration
* Average quality improves through retries
* Functions even without trend data

---

## 10. Governance Rule

If a new feature violates this document,
**the feature must be removed — not the document.**

---

## 11. Cross-Agent / Cross-API Continuity Guarantee (NEW)

To ensure safe handoff between different API agents or model versions:

* All critical context must be externalized as artifacts:

  * PROJECT_SPEC
  * DecisionPolicy
  * Skill Contracts
  * ClickThesis
* No decision may rely on unstated prior conversation
* Any new agent must be able to resume work by reading artifacts only

> If context cannot be reconstructed from files, the design is invalid.
