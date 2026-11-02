# Article OG Cover System Design

## Scope

Introduce a default visual system for new ordinary blog articles on `nasuta.ru`.

The system creates one dedicated 1200×630 JPEG for each article. That JPEG is used in the article’s Open Graph and Twitter metadata and in article cards on the home page and archive. It is not rendered inside the article body unless Pavel explicitly requests it.

Out of scope: retrofitting every existing article, changing the visual system for the cognitive-bias catalogue, products, skills, site home-page OG, or publishing to GitHub Pages.

## Visual contract

Each article cover uses a portrait-led editorial composition:

- portrait of Pavel on the left third;
- fully separate warm off-white field on the right for the article title;
- dark navy title, programmatically composited after image generation;
- small `nasuta.ru` footer in the text field;
- deep navy, warm paper, and restrained teal system marks;
- no generated Cyrillic, fake UI labels, pseudo-text, logos, watermarks, or visual elements behind the title.

The background scene is selected by article intent:

1. `overshirt-standing` for AI, processes, and management;
2. `table-knit` for analysis, research, and long-form explanation;
3. `jacket-relaxed` for opinion, notes, and experiments.

Selection is explicit in the article cover request; a future default chooser may use the article’s declared type. The generator must not claim semantic certainty from an unstructured title alone.

## Generation and asset contract

A reusable cover-generator module receives:

```python
CoverRequest(
    slug: str,
    title: str,
    variant: Literal['overshirt-standing', 'table-knit', 'jacket-relaxed'],
    output_path: Path,
)
```

It produces one `assets/images/og-<slug>.jpg` file, exactly 1200×630 pixels.

The generator takes an approved, text-free visual background for the selected portrait scene and composites exact article typography using local fonts. It validates the output dimensions and the expected title/domain text before returning the asset path. Generation backgrounds are source assets, not public default cover files.

## Site integration

For a new blog article:

- `og:image` and `twitter:image` point to `https://nasuta.ru/assets/images/og-<slug>.jpg`;
- `og:image:width` is `1200` and `og:image:height` is `630`;
- `og:image:alt` describes the article cover and author;
- article-card markup receives an optional `<img>` thumbnail that uses the same asset;
- article detail markup has no in-body `<img>` for this OG asset.

The site generator or registry must be the source of truth for these fields so a rebuild cannot discard them.

## Reference test article

Use `ai-agent-knowledge-storage` as the local proof article, with the `overshirt-standing` background and its existing visible title. The proof may update only local generated files and is not committed or published.

## Acceptance checks

1. Generated proof JPEG is exactly 1200×630 and has no accidental text or watermark beyond programmatically composited title and `nasuta.ru`.
2. Exact Russian title and `nasuta.ru` are legible in the right-side clear zone at normal and thumbnail scale.
3. Proof article metadata references the generated JPEG for both Open Graph and Twitter.
4. The same image is visible in the proof article’s home and archive cards.
5. The proof article body does not render the OG JPEG.
6. Desktop, 390px, and 360px site views have no horizontal overflow and the card remains readable.
7. No changes are committed, pushed, or published without a separate explicit instruction.
