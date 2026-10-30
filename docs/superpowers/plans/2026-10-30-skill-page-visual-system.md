# Skill Page Visual System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make every published Skill Hub detail route conform to the approved Book Summary editorial visual system.

**Architecture:** Retain the existing static HTML details and registry-driven catalogue. Centralize detail-page layout in `skills-editorial.css`, restore the live-only Metrica route as a tracked registry record, and guard the system with structural tests.

**Tech Stack:** Static HTML, CSS, Python `unittest`, Pillow, local HTTP server and browser QA.

**Spec:** `docs/superpowers/specs/2026-10-30-skill-page-visual-system-design.md`

## Global Constraints

- Do not commit, push or publish.
- Every published skill route has one shared stylesheet, an in-page rectangular 1200×630 JPEG and one canonical Lucide icon mark.
- Preserve current text, status, compatibility and repository claims unless the record is missing from the local source.

---

### Task 1: Encode the visual contract

**Files:**
- Modify: `tests/test_skill_hub_quality.py`
- Test: `tests/test_skill_hub_quality.py`

- [ ] Add assertions for all seven published records, the shared stylesheet, one `hero-mark`, the rectangular hero rule and a valid unique 1200×630 JPEG.
- [ ] Run the targeted test and confirm it fails because legacy pages and the Metrica route do not yet satisfy the contract.

### Task 2: Normalize pages and registry

**Files:**
- Modify: `data/skills.json`, `assets/styles/skills-editorial.css`, all existing `skills/*/index.html`, `sitemap.xml`
- Create: `skills/yandex-metrica-analytics-full/index.html`

- [ ] Make the shared stylesheet the only detail stylesheet.
- [ ] Apply a canonical Lucide hero mark and shared markup to each route.
- [ ] Restore Metrica to the registry, route and sitemap.
- [ ] Run the targeted test and confirm it passes.

### Task 3: Replace divergent visual assets

**Files:**
- Modify: `assets/images/og-skill-art-directing-visuals.jpg`, `assets/images/og-skill-telegram-channel-analytics.jpg`
- Create: `assets/images/og-skill-yandex-metrica-analytics-full.jpg`
- Modify: `tools/generate_skill_og_images.py`

- [ ] Create subject-specific 1200×630 imagery with no generated text or pseudo-UI.
- [ ] Inspect each image, use it in the route, and run the visual-contract test.

### Task 4: Verify rendered routes

**Files:**
- Test: `tests/test_skill_hub_quality.py`

- [ ] Run full tests, HTML/JSON-LD validation and whitespace checks.
- [ ] Render all routes locally at 360px, 390px, 768px and desktop; confirm no horizontal overflow and inspect representative screenshots.
- [ ] Review the diff for drift, secrets and regressions; prepare local review only.
