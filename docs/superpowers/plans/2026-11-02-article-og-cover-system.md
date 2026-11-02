# Article OG Cover System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a local, verified default OG-cover pipeline for new nasuta.ru blog articles, with portrait-led editorial backgrounds, exact programmatic typography, metadata integration, and card thumbnails.

**Architecture:** A focused Python cover module will composite exact headline typography and `nasuta.ru` over pre-approved text-free portrait backgrounds. The article source of truth will declare its cover asset and expose that asset in article metadata and cards, while the detail article body remains image-free. Tests will assert the asset, metadata, card usage, and no-body-image boundary.

**Tech Stack:** Python 3.11, Pillow, static HTML/CSS, existing Python `unittest` test suite, local static server and browser QA.

**Spec:** `docs/superpowers/specs/2026-11-02-article-og-cover-system-design.md`

## Global Constraints

- Generate exactly one 1200×630 JPEG per new ordinary blog article.
- Use the image only in `og:image`, `twitter:image`, home/archive cards; do not insert it in the article body.
- Keep the portrait on the left and a quiet, warm off-white title field on the right.
- Compose the exact Russian title and `nasuta.ru` programmatically; never rely on generated Cyrillic.
- Use only `overshirt-standing`, `table-knit`, and `jacket-relaxed` portrait-scene backgrounds.
- Do not commit, push, or publish any output without separate explicit Pavel approval.

---

## File Structure

- Create: `tools/article_og_cover.py` — typed cover request, background lookup, title wrapping, JPEG composition, validation.
- Create: `assets/images/article-cover-sources/overshirt-standing.jpg` — approved text-free source background.
- Create: `assets/images/article-cover-sources/table-knit.jpg` — approved text-free source background.
- Create: `assets/images/article-cover-sources/jacket-relaxed.jpg` — approved text-free source background.
- Create: `assets/images/og-ai-agent-knowledge-storage.jpg` — local proof article JPEG.
- Modify: `articles/ai-agent-knowledge-storage/index.html` — metadata only, no body insertion.
- Modify: `index.html` — proof article card thumbnail using the proof JPEG.
- Modify: `articles/index.html` — proof article card thumbnail using the proof JPEG.
- Modify: `assets/styles/style.css` or the active article-card stylesheet after inspection — card image layout and narrow-width behavior.
- Create: `tests/test_article_og_cover.py` — output dimensions, exact copy contract, route/card/body boundaries.
- Modify: `art-directing-visuals` skill — reusable cover-background art direction and rejection rules.
- Modify: `pavel-public-sites` skill — new-article OG/card integration rule and no-in-body-image boundary.

## Task 1: Inspect the proof article and card renderers

**Files:**
- Read: `articles/ai-agent-knowledge-storage/index.html`
- Read: `index.html`
- Read: `articles/index.html`
- Read: active stylesheets linked from those documents
- Read: `tests/test_ai_agent_knowledge_storage_page.py`

**Interfaces:**
- Consumes: existing proof article URL and card markup.
- Produces: exact owning files and selector names used by Tasks 3–5.

- [ ] **Step 1: Record current card and metadata contracts**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
for p in [
    Path('articles/ai-agent-knowledge-storage/index.html'),
    Path('index.html'),
    Path('articles/index.html'),
]:
    text=p.read_text(encoding='utf-8')
    print(p)
    print('og image:', 'og:image' in text)
    print('knowledge route:', 'ai-agent-knowledge-storage' in text)
PY
```

Expected: all three files are identified and the proof article currently has OG metadata.

- [ ] **Step 2: Identify active card selectors**

Read the exact linked CSS files and record the class names around the proof article card; do not create a new card system.

- [ ] **Step 3: Commit**

Do not commit during this local-only implementation. Record the inspection findings in the task handoff instead.

## Task 2: Add failing cover-pipeline tests

**Files:**
- Create: `tests/test_article_og_cover.py`

**Interfaces:**
- Consumes: `tools.article_og_cover.CoverRequest`, `render_cover`, and `validate_cover`.
- Produces: test contract for the generator and static integration.

- [ ] **Step 1: Write the failing generator test**

```python
from pathlib import Path
from PIL import Image
from tools.article_og_cover import CoverRequest, render_cover

ROOT = Path(__file__).resolve().parents[1]

def test_render_cover_writes_exact_1200_by_630_jpeg(tmp_path):
    output = tmp_path / "og-proof.jpg"
    request = CoverRequest(
        slug="proof",
        title="Агенту нужно не только помнить. Ему нужно куда складывать работу",
        variant="overshirt-standing",
        output_path=output,
    )
    render_cover(request, root=ROOT)
    assert output.is_file()
    assert Image.open(output).size == (1200, 630)
```

- [ ] **Step 2: Write the failing static-boundary tests**

```python
def test_proof_article_uses_its_own_og_cover_only_in_metadata():
    article = (ROOT / "articles/ai-agent-knowledge-storage/index.html").read_text(encoding="utf-8")
    asset = "https://nasuta.ru/assets/images/og-ai-agent-knowledge-storage.jpg"
    assert f'property="og:image" content="{asset}"' in article
    assert f'name="twitter:image" content="{asset}"' in article
    body = article.split("</head>", 1)[1]
    assert "og-ai-agent-knowledge-storage.jpg" not in body


def test_home_and_archive_cards_use_the_same_proof_cover():
    relative = "/assets/images/og-ai-agent-knowledge-storage.jpg"
    for page in (ROOT / "index.html", ROOT / "articles/index.html"):
        assert relative in page.read_text(encoding="utf-8")
```

- [ ] **Step 3: Run test to verify it fails**

Run: `python3 -m unittest tests.test_article_og_cover -v`

Expected: FAIL because `tools.article_og_cover` and the new card/metadata contract do not yet exist.

## Task 3: Implement the deterministic OG-cover generator

**Files:**
- Create: `tools/article_og_cover.py`
- Create: `assets/images/article-cover-sources/overshirt-standing.jpg`
- Create: `assets/images/article-cover-sources/table-knit.jpg`
- Create: `assets/images/article-cover-sources/jacket-relaxed.jpg`

**Interfaces:**
- Consumes: `CoverRequest(slug: str, title: str, variant: Literal[...], output_path: Path)`.
- Produces: `render_cover(request: CoverRequest, root: Path) -> Path` and `validate_cover(path: Path) -> None`.

- [ ] **Step 1: Add the request type and background mapping**

```python
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

CoverVariant = Literal["overshirt-standing", "table-knit", "jacket-relaxed"]

@dataclass(frozen=True)
class CoverRequest:
    slug: str
    title: str
    variant: CoverVariant
    output_path: Path

BACKGROUND_NAMES = {
    "overshirt-standing": "overshirt-standing.jpg",
    "table-knit": "table-knit.jpg",
    "jacket-relaxed": "jacket-relaxed.jpg",
}
```

- [ ] **Step 2: Implement programmatic composition**

Use Pillow to:

```python
def render_cover(request: CoverRequest, root: Path) -> Path:
    background = Image.open(root / "assets/images/article-cover-sources" / BACKGROUND_NAMES[request.variant]).convert("RGB")
    canvas = background.resize((1200, 630), Image.Resampling.LANCZOS)
    # Draw title only in x=690..1140 and y=120..490.
    # Use a dark navy local font, line-wrap by pixel width, and draw nasuta.ru at x=1128, y=580 with right anchor.
    # Raise ValueError when the title cannot fit into the text field with the minimum agreed size.
    canvas.save(request.output_path, "JPEG", quality=92, optimize=True)
    validate_cover(request.output_path)
    return request.output_path
```

Use a real installed serif or display font that supports Cyrillic. Keep title field exclusively clear: never draw generated background marks into `x >= 670`.

- [ ] **Step 3: Add output validation**

```python
def validate_cover(path: Path) -> None:
    image = Image.open(path)
    if image.size != (1200, 630):
        raise ValueError(f"Expected 1200×630, got {image.size}")
    if image.format != "JPEG":
        raise ValueError(f"Expected JPEG, got {image.format}")
```

- [ ] **Step 4: Add the three approved source backgrounds**

Save only text-free source imagery. Inspect each before use and reject any image containing pseudo-text, watermarks, a second person, or texture/diagram elements in the right title field.

- [ ] **Step 5: Run tests**

Run: `python3 -m unittest tests.test_article_og_cover -v`

Expected: generator dimension test PASS; static tests remain FAIL until Task 4.

## Task 4: Create the proof asset and integrate it in metadata and cards

**Files:**
- Create: `assets/images/og-ai-agent-knowledge-storage.jpg`
- Modify: `articles/ai-agent-knowledge-storage/index.html`
- Modify: `index.html`
- Modify: `articles/index.html`
- Modify: active card stylesheet identified in Task 1

**Interfaces:**
- Consumes: `render_cover()` and the current proof article/card markup.
- Produces: proof article metadata and card references to one canonical asset.

- [ ] **Step 1: Generate the proof cover**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
from tools.article_og_cover import CoverRequest, render_cover
root = Path('.')
render_cover(CoverRequest(
    slug='ai-agent-knowledge-storage',
    title='Агенту нужно не только помнить. Ему нужно куда складывать работу',
    variant='overshirt-standing',
    output_path=root / 'assets/images/og-ai-agent-knowledge-storage.jpg',
), root)
PY
```

Expected: `assets/images/og-ai-agent-knowledge-storage.jpg` exists and is 1200×630.

- [ ] **Step 2: Update article metadata**

Replace both existing proof-article image URLs with:

```html
https://nasuta.ru/assets/images/og-ai-agent-knowledge-storage.jpg
```

Preserve `og:image:width="1200"`, `og:image:height="630"`, and update `og:image:alt` to describe Pavel’s portrait-led article cover and the article title.

- [ ] **Step 3: Add the same cover as a card thumbnail**

Add one semantic thumbnail image inside the proof article’s existing link/card on the home page and archive. Use an empty `alt` only if the card title remains the accessible name; otherwise use the article title. Do not add a separate nested link.

- [ ] **Step 4: Add responsive card-image rules**

Use the existing card selector. Ensure the thumbnail does not force a fixed card height, remains `width: 100%`, has a defined crop via `object-fit: cover`, and remains readable without horizontal overflow at 360px and 390px.

- [ ] **Step 5: Run focused tests**

Run: `python3 -m unittest tests.test_article_og_cover tests.test_ai_agent_knowledge_storage_page -v`

Expected: PASS.

## Task 5: Add policy to the owning skills

**Files:**
- Modify: `art-directing-visuals/SKILL.md`
- Modify: `pavel-public-sites/SKILL.md`

**Interfaces:**
- Consumes: approved visual and integration contract from the spec.
- Produces: reusable instructions for future cover generation and site integration.

- [ ] **Step 1: Extend `art-directing-visuals`**

Add a subsection for Pavel’s ordinary blog OG covers requiring the three approved portrait variants, left portrait/right clear type field, generated text-free background, and programmatic title/domain compositing. Explicitly ban generated text, pseudo-text, watermarks, and background detail behind title copy.

- [ ] **Step 2: Extend `pavel-public-sites`**

Add a subsection requiring distinct 1200×630 JPEGs for new ordinary articles, asset references in Open Graph/Twitter plus home/archive cards, and no inline article-body insertion unless Pavel explicitly requests it. Require local visual checks before any publication.

- [ ] **Step 3: Validate both skill files**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
for path in [
    Path('/root/.hermes/skills/creative/art-directing-visuals/SKILL.md'),
    Path('/root/.hermes/skills/software-development/pavel-public-sites/SKILL.md'),
]:
    text=path.read_text(encoding='utf-8')
    assert '1200×630' in text
    assert 'nasuta.ru' in text
    print(path, 'OK')
PY
```

Expected: both files print `OK`.

## Task 6: Full local verification

**Files:**
- Test: `tests/test_article_og_cover.py`
- Test: existing test suite that covers the proof article and front-page SEO/card routes.

**Interfaces:**
- Consumes: all completed local changes.
- Produces: a local-only verification record.

- [ ] **Step 1: Run focused and full relevant test suites**

Run:

```bash
python3 -m unittest \
  tests.test_article_og_cover \
  tests.test_ai_agent_knowledge_storage_page \
  tests.test_home_article_feature \
  tests.test_seo_coverage -v
```

Expected: PASS.

- [ ] **Step 2: Parse changed HTML and check whitespace**

Run:

```bash
python3 - <<'PY'
from html.parser import HTMLParser
from pathlib import Path
class Parser(HTMLParser): pass
for p in [Path('index.html'), Path('articles/index.html'), Path('articles/ai-agent-knowledge-storage/index.html')]:
    Parser().feed(p.read_text(encoding='utf-8'))
    print(p, 'parsed')
PY
git diff --check
```

Expected: all documents parse and `git diff --check` prints nothing.

- [ ] **Step 3: Visual QA with a local static server**

Inspect the home page, article archive, and proof article at desktop, 390px, and 360px. Verify the proof thumbnail is visible and legible in cards; confirm no horizontal overflow; confirm the proof article body does not show the OG image; open the JPEG directly and verify text contrast and clean title field.

- [ ] **Step 4: Commit**

Do not commit, push, or publish. Report the local change set and verification evidence to Pavel for review.

## Self-review

- Spec coverage: Tasks 2–4 cover generation, metadata, card usage, no-body-image boundary, and source of truth; Task 5 covers skills; Task 6 covers local verification and non-publication.
- Placeholder scan: no TBD/TODO or unspecified implementation steps remain.
- Interface consistency: `CoverRequest`, `render_cover`, and `validate_cover` are defined in Task 3 and used consistently in Tasks 2 and 4.
