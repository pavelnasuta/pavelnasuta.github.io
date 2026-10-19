# Cognitive Bias Catalogue Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish and maintain 188 research-grounded cognitive-bias cards in ten verified waves.

**Architecture:** A structured registry drives deterministic static-page generation, catalogue rows, sitemap and long-form content checks. Evidence and SEO fields belong to each registry entry; reusable templates render the common layout, CTA, analytics bootstrap and metadata consistently.

**Tech Stack:** Python standard library, static HTML/CSS/inline SVG, GitHub Pages, Python `unittest`, browser verification.

**Spec:** `docs/superpowers/specs/2026-10-19-cognitive-bias-catalogue-design.md`

## Global Constraints

- The canonical production origin is `https://nasuta.ru`.
- The source list contains exactly 188 entries; existing confirmation bias and anchoring count toward wave 1.
- Each new card has one H1, unique SEO metadata, Article JSON-LD, a visible source section, an internal catalogue link, sitemap entry and exactly one Metrika loader/init/pixel for counter `27865374`.
- Catalogue category labels stay short; detail-page category labels use the four expanded Russian phrases from the spec.
- Every detail page has the common CTA with the specified channel and contact links.
- No page may include draft, forthcoming, placeholder or generation-status text.
- Publish only after all batch checks pass; start the next wave only after live verification of the previous one.

---

### Task 1: Create the structured source registry and generator contract

**Files:**
- Create: `content/biases/catalogue.json`
- Create: `tools/build_biases.py`
- Create: `tests/test_biases_catalogue.py`
- Modify: `tests/test_biases_preview.py`

**Interfaces:**
- `content/biases/catalogue.json` is a JSON object with `items`, an array of 188 identity objects; only entries with `published: true` must contain the complete editorial fields and may be rendered.
- Every card has `slug`, `russian_name`, `english_name`, `catalogue_category`, `detail_category`, `problem`, `lede`, `scenario`, `mechanism`, `watch_for`, `helps`, `status_note`, `sources`, `seo`, and `diagram`.
- `tools/build_biases.py` exposes `load_catalogue(path)`, `validate_catalogue(items)`, `render_detail(item, previous, next_item)`, and `build(root, catalogue)`.

- [ ] **Step 1: Write the failing registry-contract tests**

```python
def test_catalogue_has_exactly_188_unique_identities_and_complete_published_items(self):
    items = json.loads((ROOT / 'content/biases/catalogue.json').read_text())['items']
    self.assertEqual(len(items), 188)
    self.assertEqual(len({item['slug'] for item in items}), 188)
    for item in items:
        self.assertTrue(item['russian_name'])
        if item['published']:
            self.assertTrue(item['sources'])
            self.assertIn(item['detail_category'], DETAIL_CATEGORIES)
```

- [ ] **Step 2: Run the contract tests and verify the expected failure**

Run: `python -m unittest tests.test_biases_catalogue -v`

Expected: failure because the registry does not exist.

- [ ] **Step 3: Implement the schema validator and seed the 188 canonical names**

```python
def validate_catalogue(items):
    required = {'slug', 'russian_name', 'english_name', 'catalogue_category',
                'detail_category', 'lede', 'scenario', 'mechanism', 'watch_for',
                'helps', 'status_note', 'sources', 'seo', 'diagram'}
    assert len(items) == 188
    assert len({item['slug'] for item in items}) == 188
    for item in items:
        missing = required - item.keys()
        if missing or not item['sources']:
            raise ValueError(f"Incomplete entry: {item.get('slug')}: {missing}")
```

- [ ] **Step 4: Run the registry tests and verify they pass**

Run: `python -m unittest tests.test_biases_catalogue -v`

Expected: PASS.

- [ ] **Step 5: Commit the generator foundation**

```bash
git add content/biases/catalogue.json tools/build_biases.py tests/test_biases_catalogue.py tests/test_biases_preview.py
git commit -m "feat: add cognitive biases content registry"
```

### Task 2: Build one reusable detail-page template, CTA and catalogue renderer

**Files:**
- Modify: `tools/build_biases.py`
- Modify: `assets/styles/biases.css`
- Modify: `biases/index.html`
- Create: `tests/test_biases_template.py`

**Interfaces:**
- `render_detail` writes `biases/<slug>/index.html`.
- `render_catalogue` writes a linked `a.bias-row` for every published card.
- `render_cta` outputs the identical semantic CTA block on every detail page.

- [ ] **Step 1: Write failing template tests**

```python
def test_rendered_card_has_expanded_category_cta_and_seo(self):
    html = render_detail(sample_item, None, None)
    self.assertIn('Когда не хватает смысла', html)
    self.assertIn('Персональный тренер для вашего агента', html)
    self.assertIn('https://t.me/niimozgii', html)
    self.assertIn('https://t.me/pavelnasuta', html)
    self.assertIn('https://www.linkedin.com/in/nasuta', html)
    self.assertIn('mailto:pavelnasuta@gmail.com', html)
```

- [ ] **Step 2: Run template tests and verify the expected failure**

Run: `python -m unittest tests.test_biases_template -v`

Expected: failure because the renderer has not created the CTA and expanded category labels.

- [ ] **Step 3: Implement semantic rendering and mobile rhythm**

```python
def render_cta():
    return '''<aside class="bias-cta" aria-label="О Павле Насуте">
      <p class="bias-cta__label">НИИ «МОЗГИ»</p>
      <h2>Персональный тренер для вашего агента</h2>
      <p>Павел Насута — AI-powered product builder.</p>
      <a class="bias-cta__button" href="https://t.me/niimozgii" target="_blank" rel="noopener">Открыть канал ↗</a>
    </aside>'''
```

Use `.article-head .eyebrow`, `.article h1`, and `.article-dek` as separate spacing targets. Do not alter catalogue labels.

- [ ] **Step 4: Run template and existing tests**

Run: `python -m unittest discover -s tests -v`

Expected: PASS.

- [ ] **Step 5: Commit the reusable page system**

```bash
git add tools/build_biases.py assets/styles/biases.css biases/index.html tests/test_biases_template.py
git commit -m "feat: add reusable cognitive bias page template"
```

### Task 3: Add content validation for SEO/GEO, sources, CTA, analytics and draft text

**Files:**
- Create: `tests/test_biases_quality.py`
- Modify: `tests/test_seo_coverage.py`
- Modify: `tests/test_yandex_metrika.py`

**Interfaces:**
- `published_bias_pages()` returns each generated bias HTML path.
- The quality suite fails for incomplete metadata, missing CTA/contact link, absent named source, missing Metrika, malformed JSON-LD, unlisted sitemap URL or forbidden draft language.

- [ ] **Step 1: Write failing quality checks**

```python
def test_each_published_bias_has_visible_evidence_and_required_cta(self):
    for page in published_bias_pages():
        html = page.read_text(encoding='utf-8').lower()
        self.assertIn('что известно и откуда', html)
        self.assertIn('персональный тренер для вашего агента', html)
        self.assertNotRegex(html, r'чернов|в разработке|добавим|заполнить|placeholder')
```

- [ ] **Step 2: Run the new suite and verify it fails before the template is complete**

Run: `python -m unittest tests.test_biases_quality -v`

Expected: failure naming the missing requirement.

- [ ] **Step 3: Implement the quality helpers and metadata assertions**

```python
def assert_one_metrika(html):
    assert html.count('https://mc.yandex.ru/metrika/tag.js') == 1
    assert html.count("ym(27865374, 'init'") == 1
    assert html.count('https://mc.yandex.ru/watch/27865374') == 1
```

Parse every JSON-LD block through `json.loads`; parse `sitemap.xml` through `xml.etree.ElementTree`.

- [ ] **Step 4: Run the full test suite**

Run: `python -m unittest discover -s tests -v`

Expected: PASS.

- [ ] **Step 5: Commit automated quality gates**

```bash
git add tests/test_biases_quality.py tests/test_seo_coverage.py tests/test_yandex_metrika.py
git commit -m "test: guard cognitive bias content quality"
```

### Task 4: Research, generate, test and publish each 20-card wave

**Files per wave:**
- Modify: `content/biases/catalogue.json`
- Generate: `biases/<slug>/index.html` for all cards in the wave
- Modify: `biases/index.html`, `sitemap.xml`, `llms.txt`
- Modify: `assets/images/biases/<slug>.svg` only when a diagram passes the necessity test

**Interfaces:**
- Each wave has `published_count` values `20, 40, 60, 80, 100, 120, 140, 160, 180, 188`.
- Source URLs are specific to each card; no generic bibliography substitutes for per-card evidence.

- [ ] **Step 1: Research the next wave before writing copy**

For every item, capture the source type, named authors, year, stable URL/DOI, a cautious scientific-status note, and a decision-relevant scenario. Mark only diagrams that explain a causal or quantitative relationship.

- [ ] **Step 2: Write failing count and route tests for each concrete wave target**

```python
TARGETS = (20, 40, 60, 80, 100, 120, 140, 160, 180, 188)

def test_wave_has_expected_number_of_published_bias_routes(self):
    self.assertIn(len(published_bias_pages()), TARGETS)
    self.assertEqual(len(re.findall(r'<a class="bias-row"', catalogue_html)), len(published_bias_pages()))
```

Before every wave, set the test's one allowed `target` value in sequence: 20, then 40, 60, 80, 100, 120, 140, 160, 180 and 188.

- [ ] **Step 3: Fill the validated registry data and run the generator for the concrete target**

Run these exact commands in order as waves complete:

```bash
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 20
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 40
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 60
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 80
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 100
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 120
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 140
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 160
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 180
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count 188
```

Expected: generation stops with a non-zero exit code if a card lacks any required content or a valid source URL.

- [ ] **Step 4: Run all automated checks and inspect real routes at 360px, 390px, 768px and desktop**

Run: `python -m unittest discover -s tests -v && git diff --check`

Exercise catalogue search/filter, first and last new card, internal previous/next/random navigation, CTA links and Metrika bootstrap.

- [ ] **Step 5: Commit and publish each complete wave**

Use these ten commit messages in order:

```text
feat: publish cognitive biases wave 1
feat: publish cognitive biases wave 2
feat: publish cognitive biases wave 3
feat: publish cognitive biases wave 4
feat: publish cognitive biases wave 5
feat: publish cognitive biases wave 6
feat: publish cognitive biases wave 7
feat: publish cognitive biases wave 8
feat: publish cognitive biases wave 9
feat: publish cognitive biases wave 10
```

For every wave, run:

```bash
git add content/biases/catalogue.json biases/ sitemap.xml llms.txt assets/images/biases/ tests/
git commit -m "the matching wave message above"
git fetch origin
git rebase origin/main
git push origin main
```

- [ ] **Step 6: Verify the live custom domain before starting the next wave**

Wait for the exact GitHub Pages deployment after each of the ten commits. Load the catalogue with `?wave=1` through `?wave=10` respectively, then the first and last new detail URL. Assert the matching live totals 20, 40, 60, 80, 100, 120, 140, 160, 180 and 188; CTA, no draft language, canonical `https://nasuta.ru/...`, parsed JSON-LD and `typeof window.ym === 'function'`.

### Task 5: Perform a complete post-publication audit

**Files:**
- Modify only if audit finds a defect: `content/biases/catalogue.json`, generated files, tests, sitemap or styles.

- [ ] **Step 1: Add a final 188-card regression test**

```python
def test_all_188_cards_are_linked_indexable_and_not_drafts(self):
    self.assertEqual(len(published_bias_pages()), 188)
    for page in published_bias_pages():
        html = page.read_text(encoding='utf-8').lower()
        self.assertNotRegex(html, r'чернов|в разработке|добавим|placeholder')
```

- [ ] **Step 2: Run the full suite and static validation**

Run: `python -m unittest discover -s tests -v && git diff --check`

Expected: PASS with 188 bias routes covered.

- [ ] **Step 3: Verify sampled live routes across all four Codex problems and the final route**

Use the live domain to inspect a route from every expanded category, the first card, the 188th card and the catalogue. Verify CTA, analytics, metadata and no draft language.

- [ ] **Step 4: Commit any audit repairs and verify the exact live deployment**

```bash
git add -A
git commit -m "fix: complete cognitive biases catalogue audit"
git push origin main
```
