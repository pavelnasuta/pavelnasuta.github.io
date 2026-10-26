# Telegram Channel Analytics Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish a portable, read-only Telegram channel analytics skill with an honest weekly report, append-only evidence, delayed post measurements, and an optional comparable-channel watchlist.

**Architecture:** The public repository is built in its own standalone local package workspace, never inside the static-site checkout. A canonical `SKILL.md` describes the workflow; JSON templates define durable artifacts; a stdlib Python validator checks project integrity offline. The existing static site exposes only the released package through the Skill Hub registry, a Russian explanation page, and a unique social image.

**Tech Stack:** Markdown, JSON, Python standard library/unittest, static HTML/CSS, Pillow, GitHub CLI, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-10-26-telegram-channel-analytics-design.md`

## Global Constraints

- `telegram-channel-analytics` is read-only: no post publication, Telegram user session, MTProto, `api_id`, `api_hash`, session file, or native-statistics claim.
- All public examples and test fixtures are synthetic; do not publish real channels, data, credentials, personal settings, or absolute local paths.
- Snapshots are append-only; derived reports name their input snapshots; methodology/source changes create a distinct series.
- Comparative analysis requires an explicitly versioned watchlist and produces hypotheses, never rankings or causal proof.
- Public repository identity: `pavelnasuta/telegram-channel-analytics-skill`; license: MIT; release: `v1.0.0`.
- The site page, card, and public README describe only verified release capability in Russian on the site and English in the repository.

---

### Task 1: Package contract and validator tests

**Files:**
- Create: `tests/test_public_package.py`
- Create: `tests/test_validate_project.py`
- Create: `skills/telegram-channel-analytics/templates/project.schema.json`
- Create: `skills/telegram-channel-analytics/templates/snapshot.schema.json`
- Create: `skills/telegram-channel-analytics/templates/watchlist.schema.json`
- Create: `skills/telegram-channel-analytics/templates/weekly-report.template.md`
- Create: `skills/telegram-channel-analytics/scripts/validate_project.py`

**Interfaces:**
- Consumes: a project directory with `project.json`, `snapshots/posts/*.json`, optional `watchlists/*.json`, and reports with `inputs` manifests.
- Produces: `validate_project(project_dir: pathlib.Path) -> list[str]`, where an empty list means all checked invariants hold.

- [ ] **Step 1: Write the failing package-contract test.**

```python
def test_canonical_skill_declares_read_only_evidence_workflow():
    skill = (ROOT / "skills/telegram-channel-analytics/SKILL.md").read_text(encoding="utf-8")
    assert "append-only" in skill
    assert "24 hours" in skill
    assert "7 days" in skill
    assert "14 days" in skill
    assert "watchlist" in skill
    assert "MTProto" in skill
```

- [ ] **Step 2: Run the package-contract test to verify it fails.**

Run: `python3 -m unittest tests/test_public_package.py -v`

Expected: FAIL because the canonical skill does not exist.

- [ ] **Step 3: Write failing validator tests for valid data and four boundary violations.**

```python
def test_valid_project_passes(tmp_path):
    make_valid_project(tmp_path)
    assert validate_project(tmp_path) == []

def test_snapshot_without_source_is_rejected(tmp_path):
    make_valid_project(tmp_path, snapshot_overrides={"source": ""})
    assert "source" in "\n".join(validate_project(tmp_path))

def test_duplicate_snapshot_id_is_rejected(tmp_path):
    make_valid_project(tmp_path, duplicate_snapshot_id=True)
    assert "duplicate" in "\n".join(validate_project(tmp_path)).lower()

def test_comparative_report_requires_versioned_watchlist(tmp_path):
    make_valid_project(tmp_path, report_mode="comparative", write_watchlist=False)
    assert "watchlist" in "\n".join(validate_project(tmp_path)).lower()

def test_report_inputs_must_reference_existing_snapshots(tmp_path):
    make_valid_project(tmp_path, report_input="missing.json")
    assert "input" in "\n".join(validate_project(tmp_path)).lower()
```

- [ ] **Step 4: Run validator tests to verify they fail because the validator does not exist.**

Run: `python3 -m unittest tests/test_validate_project.py -v`

Expected: FAIL with an import or missing-module error for `validate_project`.

- [ ] **Step 5: Implement only the JSON templates and stdlib validator needed for the tests.**

```python
def validate_project(project_dir: Path) -> list[str]:
    errors: list[str] = []
    # read declared project, every snapshot, every watchlist and every report
    # enforce source/method/collected_at/snapshot_id uniqueness
    # require report input paths to exist
    # require a versioned watchlist for comparative reports
    return errors
```

- [ ] **Step 6: Run focused tests, then the full package suite.**

Run: `python3 -m unittest tests/test_public_package.py tests/test_validate_project.py -v`

Expected: PASS with all contract and validator tests green.

- [ ] **Step 7: Commit the tested data contract.**

```bash
git add tests skills/telegram-channel-analytics/templates skills/telegram-channel-analytics/scripts
git commit -m "feat: add analytics evidence validator"
```

### Task 2: Canonical skill, adapters, documentation and privacy scan

**Files:**
- Create: `skills/telegram-channel-analytics/SKILL.md`
- Create: `agents/claude-code/SKILL.md`
- Create: `agents/codex/AGENTS.md`
- Create: `agents/agents-md/AGENTS.md`
- Create: `README.md`
- Create: `LICENSE`
- Create: `.gitignore`
- Modify: `tests/test_public_package.py`

**Interfaces:**
- Consumes: a channel URL, project directory and explicitly chosen source/watchlist policy.
- Produces: stored immutable snapshots and weekly/monthly/yearly reports built only from those inputs.

- [ ] **Step 1: Add failing tests for adapters, public README and privacy boundaries.**

```python
def test_adapters_point_to_the_canonical_workflow():
    for path in ADAPTERS:
        assert "skills/telegram-channel-analytics/SKILL.md" in path.read_text(encoding="utf-8")

def test_public_files_have_no_private_or_local_markers():
    text = public_text()
    for marker in ("/root/", "api_hash", "api_id", "session", "t.me/s/real"):
        assert marker not in text

def test_readme_documents_install_limitations_and_v1_release_notes():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "v1.0.0" in readme
    assert "Privacy" in readme
    assert "Limitations" in readme
    assert "hermes skills install" in readme
```

- [ ] **Step 2: Run the expanded package suite to verify it fails.**

Run: `python3 -m unittest discover -s tests -v`

Expected: FAIL because the canonical skill, adapters, README and license are absent.

- [ ] **Step 3: Write the smallest complete canonical skill and thin adapters.**

The skill must name the project setup inputs, public-source boundaries, append-only snapshot procedure, 0h/24h/7d/14d/monthly remeasurement schedule, weekly→monthly→yearly roll-up, watchlist criteria, report structure, missing-data treatment and verification. It must explicitly prohibit personal Telegram sessions, native-analytics claims and causal assertions.

- [ ] **Step 4: Write the README, MIT license and ignore rules.**

The README must document direct installation from `pavelnasuta/telegram-channel-analytics-skill`, synthetic/offline tests, privacy boundaries, project configuration, support through GitHub Issues and `v1.0.0` release notes. `.gitignore` excludes bytecode and user project data.

- [ ] **Step 5: Run the package suite and a separate privacy scan.**

Run: `python3 -m unittest discover -s tests -v && ! rg -n '/root/|api_hash|api_id|\.session|t\.me/s/' --glob '!tests/**' .`

Expected: PASS; scan produces no matching public content.

- [ ] **Step 6: Commit the public operating contract.**

```bash
git add .
git commit -m "feat: document Telegram channel analytics workflow"
```

### Task 3: Skill Hub registry, public page and social asset

**Files:**
- Create: `tests/test_telegram_channel_analytics_page.py`
- Modify: `data/skills.json`
- Create: `skills/telegram-channel-analytics/index.html`
- Create: `assets/styles/skills-telegram-channel-analytics-index.css`
- Modify: `tools/generate_skill_og_images.py`
- Create: `assets/images/og-skill-telegram-channel-analytics.jpg`
- Modify: `index.html`
- Modify: `skills/index.html`
- Modify: `sitemap.xml`
- Modify: relevant existing Skill Hub tests

**Interfaces:**
- Consumes: the released registry entry and public repository URL.
- Produces: a local documentation route, discoverable Hub card, home-page card and unique 1200×630 OG image.

- [ ] **Step 1: Write a failing site test for all released-skill surfaces.**

```python
def test_telegram_channel_analytics_is_a_public_skill():
    item = registry_by_slug("telegram-channel-analytics")
    assert item["status"] == "released"
    assert item["visibility"] == "public"
    assert item["repository_url"] == "https://github.com/pavelnasuta/telegram-channel-analytics-skill"
    assert (ROOT / item["page_url"]).exists()

def test_detail_page_has_truthful_metadata_and_boundaries():
    page = read_page("skills/telegram-channel-analytics/index.html")
    assert 'og-skill-telegram-channel-analytics.jpg' in page
    assert "append-only" in page
    assert "MTProto" in page
    assert "GitHub" in page
```

- [ ] **Step 2: Run the focused site test to verify it fails.**

Run: `python3 -m unittest tests/test_telegram_channel_analytics_page.py -v`

Expected: FAIL because neither registry record nor route exists.

- [ ] **Step 3: Update the registry and build the Russian page.**

Set `status: released`, `visibility: public`, `source_status: published`, `version: 1.0.0`, `license: MIT`, `privacy_review: approved`, and the exact repository/page URLs. Page copy explains the weekly report, live-post measurements, durable history, watchlist comparison and limits; it includes canonical, OG/Twitter metadata, JSON-LD and a separate GitHub link.

- [ ] **Step 4: Generate, inspect and wire the individual social image.**

Add a dedicated generator function that writes `og-skill-telegram-channel-analytics.jpg` at 1200×630. The mechanism is a post timeline with accumulating observation dots and a visibly separate non-ranking watchlist contour. Use the file in hero and social metadata.

- [ ] **Step 5: Regenerate the Skill Hub and add the home-page card.**

Run the existing skills builder after registry changes. Update only its generated outputs and expected card counts/slugs in relevant tests.

- [ ] **Step 6: Run focused and complete site tests.**

Run: `python3 -m unittest tests/test_telegram_channel_analytics_page.py -v && python3 -m unittest discover -s tests -v && git diff --check`

Expected: PASS with a clean whitespace check.

- [ ] **Step 7: Visually verify at desktop and mobile.**

Run a local static server. Inspect `/skills/telegram-channel-analytics/`, `/skills/` and the home Skill Hub surface at 390px, 768px and desktop; confirm no horizontal overflow, working navigation, legible headings and loading OG image.

- [ ] **Step 8: Commit the verified site changes.**

```bash
git add data/skills.json skills/telegram-channel-analytics assets index.html sitemap.xml tests tools
git commit -m "feat: publish Telegram Channel Analytics in Skill Hub"
```

### Task 4: Public remote, tag, deployment and read-back

**Files:**
- Modify: public package repository Git metadata
- Modify: site repository Git metadata

**Interfaces:**
- Consumes: passing local package/site suites and clean release files.
- Produces: public GitHub source repository, annotated `v1.0.0` tag, successful GitHub Pages deployment and live site route.

- [ ] **Step 1: Verify package and site trees are clean apart from intended commits.**

Run: `git status --short --branch` in both repositories; run their complete test suites again.

Expected: no uncommitted release files and all verification commands exit 0.

- [ ] **Step 2: Create the public GitHub repository from the local package and verify it by read-back.**

Run: `gh repo create pavelnasuta/telegram-channel-analytics-skill --public --source . --push`

Then read back with `gh repo view pavelnasuta/telegram-channel-analytics-skill --json url,visibility,defaultBranch,description` and confirm README, LICENSE and the canonical skill through the GitHub contents API.

- [ ] **Step 3: Tag the first release and verify it.**

Run: `git tag -a v1.0.0 -m 'Telegram Channel Analytics v1.0.0' && git push origin v1.0.0`

Then read back with `gh release create v1.0.0 --title 'v1.0.0' --generate-notes` and `gh release view v1.0.0`.

- [ ] **Step 4: Rebase the site onto its current remote, push and verify the exact remote revision.**

Run: `git pull --rebase origin main && git push origin main && git ls-remote origin refs/heads/main`

Expected: local HEAD equals the remote `main` revision.

- [ ] **Step 5: Wait for Pages and verify the live custom domain.**

Use `gh run list` and `gh run watch` for the exact site push. Fetch `https://nasuta.ru/skills/telegram-channel-analytics/?v=1` and its OG JPEG; then use browser inspection to confirm the title, canonical, GitHub link, installation command, Hub card and home-page card.

- [ ] **Step 6: Run final release evidence checks and report only verified scope.**

Run package tests, site suite, privacy scan, `git diff --check`, remote API read-backs and live route checks once more. Report the public source URL, live page URL, verified limitations and any remaining non-release scope.
