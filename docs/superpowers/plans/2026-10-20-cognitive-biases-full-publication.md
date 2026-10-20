# Cognitive Biases Full Publication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish 188 evidence-grounded cognitive-bias cards in ten verified waves, with consistent CTA, SEO/GEO, analytics, expanded detail categories and no draft language.

**Architecture:** `content/biases/catalogue.json` remains the sole content registry. `tools/build_biases.py` validates the registry and renders the public catalogue and detail routes; the generator owns all repeated metadata, CTA, navigation and Metrika markup. Tests establish every release invariant before generated files are committed and the custom domain is checked after each wave.

**Tech Stack:** Python standard library, static HTML/CSS/inline SVG, Python `unittest`, GitHub Pages, browser verification.

**Spec:** `docs/superpowers/specs/2026-10-20-biases-catalogue-design.md`

## Global Constraints

- Production canonical origin is `https://nasuta.ru`.
- The registry contains exactly 188 unique safe slugs; wave targets are `20, 40, 60, 80, 100, 120, 140, 160, 180, 188`.
- Catalogue labels remain short; detail categories are exactly `Когда информации слишком много`, `Когда не хватает смысла`, `Когда нужно действовать быстро`, `Когда мы решаем, что запомнить`.
- Every detail page has one H1, source links, Article JSON-LD, canonical/OG/Twitter metadata, one Metrika loader/init/pixel, common CTA, and no draft language.
- The CTA uses `https://t.me/niimozgii`, `https://t.me/pavelnasuta`, `https://www.linkedin.com/in/nasuta`, and `mailto:pavelnasuta@gmail.com`.
- Do not alter short root-catalogue category labels.
- Preserve unrelated working-tree changes until they have been read and intentionally incorporated.

---

### Task 1: Complete and lock the generator contract

**Files:**
- Modify: `tools/build_biases.py`
- Modify: `tests/test_biases_catalogue.py`
- Modify: `tests/test_biases_template.py`
- Create: `tests/test_biases_quality.py`

**Interfaces:**
- `build(root, catalogue, expected_count=188) -> list[Path]` always renders `biases/index.html`, removes only stale generated `biases/*/index.html` routes, and returns every generated route.
- `render_detail(item, previous, next_item) -> str` emits one full article page.
- `published_bias_pages() -> list[Path]` exposes generated published cards for quality tests.

- [ ] **Step 1: Add the failing contract tests for the requested page changes.**

```python
def test_detail_template_has_expanded_category_header_spacing_and_cta(self):
    html = render_detail(sample_item, None, None)
    self.assertIn('Когда не хватает смысла', html)
    self.assertIn('class="article-head"', html)
    self.assertIn('Персональный тренер для вашего агента', html)
    for url in ('https://t.me/niimozgii', 'https://t.me/pavelnasuta',
                'https://www.linkedin.com/in/nasuta', 'mailto:pavelnasuta@gmail.com'):
        self.assertIn(url, html)
```

- [ ] **Step 2: Run the targeted tests and confirm RED.**

Run: `python -m unittest tests.test_biases_catalogue tests.test_biases_template -v`

Expected: failure that identifies the current build or template omission; correct any test import errors first without weakening assertions.

- [ ] **Step 3: Implement minimal renderer and generator corrections.**

```python
def build(root, catalogue, *, expected_count=188):
    items = list(catalogue)
    validate_catalogue(items, expected_count=expected_count)
    published = [item for item in items if item['published']]
    remove_only_generated_detail_routes(Path(root), {item['slug'] for item in published})
    catalogue_path = Path(root) / 'biases' / 'index.html'
    catalogue_path.write_text(render_catalogue(items), encoding='utf-8')
    return [catalogue_path, *render_published_details(Path(root), published)]
```

Make the detail-header category, H1 and lead separate layout targets in CSS. Add the CTA after the evidence section and before continuation navigation. Keep SVG diagrams optional and semantic.

- [ ] **Step 4: Run all generator and template tests.**

Run: `python -m unittest tests.test_biases_catalogue tests.test_biases_template -v`

Expected: PASS.

- [ ] **Step 5: Commit only generator foundation files.**

```bash
git add tools/build_biases.py assets/styles/biases.css tests/test_biases_catalogue.py tests/test_biases_template.py
git commit -m "feat: complete cognitive bias page generator"
```

### Task 2: Add release quality gates

**Files:**
- Create: `tests/test_biases_quality.py`
- Modify: `tests/test_seo_coverage.py`
- Modify: `tests/test_yandex_metrika.py`
- Modify: `tools/build_biases.py`

**Interfaces:**
- `published_bias_pages()` returns one route per `published: true` registry item.
- `refresh_sitemap(items, root)` writes a sorted, parseable sitemap including catalogue and every published route.

- [ ] **Step 1: Write failing quality assertions.**

```python
def test_published_cards_have_required_metadata_cta_and_no_draft_language(self):
    for page in published_bias_pages():
        html = page.read_text(encoding='utf-8').lower()
        self.assertIn('персональный тренер для вашего агента', html)
        self.assertEqual(html.count('https://mc.yandex.ru/metrika/tag.js'), 1)
        self.assertNotRegex(html, r'чернов|в разработке|в сборке|добавим|placeholder')
        for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
            json.loads(block)
```

- [ ] **Step 2: Run it and confirm it fails before sitemap and all-route checks exist.**

Run: `python -m unittest tests.test_biases_quality -v`

Expected: failure naming the missing quality guard.

- [ ] **Step 3: Implement sitemap refresh and full-card validators.**

```python
def refresh_sitemap(items, root):
    urls = ['https://nasuta.ru/biases/']
    urls += [f"https://nasuta.ru/biases/{item['slug']}/" for item in items if item['published']]
    write_sitemap_xml(Path(root) / 'sitemap.xml', urls)
```

Require non-empty source URL/citation, SEO title/description, expanded detail category, all CTA links and valid diagram shape before publication.

- [ ] **Step 4: Run the entire suite.**

Run: `python -m unittest discover -s tests -v && git diff --check`

Expected: PASS.

- [ ] **Step 5: Commit the release guards.**

```bash
git add tests/test_biases_quality.py tests/test_seo_coverage.py tests/test_yandex_metrika.py tools/build_biases.py
git commit -m "test: enforce cognitive bias publication quality"
```

### Task 3: Publish each evidence-reviewed wave

**Files per wave:**
- Modify: `content/biases/catalogue.json`
- Generate: `biases/index.html` and `biases/<slug>/index.html`
- Modify: `sitemap.xml`, `llms.txt` when route coverage changes
- Create only when explanatory: `assets/images/biases/<slug>.svg`

**Interfaces:**
- A published entry has all editorial fields, one or more source objects, SEO object, `diagram: null` or an accessible SVG descriptor.
- The ten exact target totals are `20, 40, 60, 80, 100, 120, 140, 160, 180, 188`.

- [ ] **Step 1: Research the next unpublished sequence.**

For each item collect a DOI, publisher record, scholarly review, or authoritative research-library URL; write a cautious status note where the Codex term is disputed, popularized, duplicated, or not a standalone bias.

- [ ] **Step 2: Write the failing target-count test before changing registry content.**

```python
def test_release_target_is_exactly_20_cards(self):
    published = [item for item in load_catalogue(CATALOGUE) if item['published']]
    self.assertEqual(len(published), 20)
```

For each later wave, replace `20` with the next value in the exact sequence above, run it and observe failure before setting more entries to `published: true`.

- [ ] **Step 3: Fill editorial fields and generate the wave.**

```bash
python tools/build_biases.py --root . --catalogue content/biases/catalogue.json --published-count TARGET
```

`TARGET` is the current exact wave total. Create an inline SVG only when it explains a comparison, timeline, base-rate split, anchoring adjustment or another mechanism more clearly than prose; give it a visible caption and text equivalent.

- [ ] **Step 4: Validate locally.**

Run: `python -m unittest discover -s tests -v && git diff --check`

Use browser checks at 360px, 390px, 768px and desktop: no horizontal overflow; 44px minimum controls; catalogue search/filter; first/last new card; previous/next/random; CTA; Metrika bootstrap.

- [ ] **Step 5: Commit and publish the wave.**

```bash
git add content/biases/catalogue.json biases/ sitemap.xml llms.txt assets/images/biases/ tests/
git commit -m "feat: publish cognitive biases wave N"
git fetch origin
git rebase origin/main
git push origin main
```

- [ ] **Step 6: Verify the live custom domain.**

Wait for the GitHub Pages deployment for the pushed revision. With a cache-busting query, assert the live catalogue has `TARGET` `a.bias-row` links and live first/last route has a canonical custom-domain URL, CTA, no draft language, parsed JSON-LD and `typeof window.ym === 'function'`. Begin the next wave only after this passes.

### Task 4: Complete the 188-card audit

**Files:**
- Modify only if a defect is detected: registry, generator, styles, generated routes, sitemap or tests.

- [ ] **Step 1: Add final count and draft-text regression test.**

```python
def test_complete_catalogue_has_188_live_ready_cards_without_draft_copy(self):
    pages = published_bias_pages()
    self.assertEqual(len(pages), 188)
    for page in pages:
        self.assertNotRegex(page.read_text(encoding='utf-8').lower(),
                            r'чернов|в разработке|в сборке|добавим|placeholder')
```

- [ ] **Step 2: Run full static validation.**

Run: `python -m unittest discover -s tests -v && git diff --check`

Expected: PASS with 188 generated routes, sitemap coverage, valid JSON-LD and exactly one Metrika bootstrap per indexable route.

- [ ] **Step 3: Inspect live samples and final catalogue.**

Load the catalogue, the first and last cards, and one card in each of the four detail categories. Confirm CTA/contact links, no draft copy, semantic headers, canonical URLs and analytics bootstrap.

- [ ] **Step 4: Commit only audit repairs and verify the resulting live deployment.**

```bash
git add content/biases/catalogue.json tools/build_biases.py assets/styles/biases.css biases/ sitemap.xml tests/
git commit -m "fix: complete cognitive biases catalogue audit"
git push origin main
```
