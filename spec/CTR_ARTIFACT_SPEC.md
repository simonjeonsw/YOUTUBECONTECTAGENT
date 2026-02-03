# /spec/CTR_ARTIFACT_SPEC.md

# CTR Artifact — Minimal Canonical Spec

## Purpose

A CTR Artifact represents **one atomic click decision unit**:
what the viewer sees and decides to click or ignore.

This spec defines the **minimum stable shape**
that all CTR-related skills must eventually converge to.

---

## Core Fields (Required)

```json
{
  "hook": "string",
  "title": "string",
  "thumbnail_text": "string"
}
Optional Metadata (Phase2+)
{
  "ctr_score": "float | null",
  "eval_signals": "object | null",
  "viewer_intent": "string | null",
  "source_skill": "string",
  "version": "string"
}
Design Principles
A CTR Artifact is immutable once created

Evaluation creates new metadata, not mutations

Skills may generate candidates, but only Artifacts are ranked or stored

Phase Policy
Phase1: Spec exists, no enforcement

Phase2: RankingSkill operates on Artifacts

Phase3: Storage + feedback loops

Phase4: Personalization & optimization

Compatibility Guarantee
Any future CTR system must:

Accept this structure

Produce this structure

Never break core fields