"""Validate the cognitive-bias registry before later rendering tasks use it."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


DETAIL_CATEGORIES = frozenset(
    {
        "Когда информации слишком много",
        "Когда не хватает смысла",
        "Когда нужно действовать быстро",
        "Когда мы решаем, что запомнить",
    }
)

IDENTITY_FIELDS = frozenset(
    {
        "slug",
        "russian_name",
        "english_name",
        "catalogue_category",
        "detail_category",
        "problem",
        "published",
    }
)
EDITORIAL_FIELDS = frozenset(
    {
        "lede",
        "scenario",
        "mechanism",
        "watch_for",
        "helps",
        "status_note",
        "sources",
        "seo",
        "diagram",
    }
)


def load_catalogue(path: str | Path) -> list[dict[str, Any]]:
    """Load the registry object and return its ordered identity records."""
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("items"), list):
        raise ValueError("Catalogue must be a JSON object with an items array")
    return document["items"]


def validate_catalogue(
    items: Iterable[dict[str, Any]], *, expected_count: int = 188
) -> None:
    """Reject malformed identities and incomplete entries marked for publication."""
    entries = list(items)
    if len(entries) != expected_count:
        raise ValueError(f"Catalogue must contain exactly {expected_count} entries")

    slugs: set[str] = set()
    for item in entries:
        if not isinstance(item, dict):
            raise ValueError("Catalogue entries must be JSON objects")
        missing_identity = IDENTITY_FIELDS - item.keys()
        if missing_identity:
            raise ValueError(
                f"Incomplete identity: {item.get('slug', '<unknown>')}: "
                f"{sorted(missing_identity)}"
            )
        if not isinstance(item["slug"], str) or not item["slug"].strip():
            raise ValueError("Every identity requires a non-empty slug")
        if item["slug"] in slugs:
            raise ValueError(f"Duplicate slug: {item['slug']}")
        slugs.add(item["slug"])
        for field in IDENTITY_FIELDS - {"slug", "published"}:
            if not isinstance(item[field], str) or not item[field].strip():
                raise ValueError(f"Identity field is empty: {item['slug']}: {field}")
        if not isinstance(item["published"], bool):
            raise ValueError(f"published must be a boolean: {item['slug']}")
        if not item["published"]:
            continue

        missing_editorial = EDITORIAL_FIELDS - item.keys()
        if missing_editorial:
            raise ValueError(
                f"Incomplete published entry: {item['slug']}: "
                f"{sorted(missing_editorial)}"
            )
        if item["detail_category"] not in DETAIL_CATEGORIES:
            raise ValueError(f"Unknown detail category: {item['slug']}")
        for field in EDITORIAL_FIELDS - {"sources", "seo", "diagram"}:
            if not isinstance(item[field], str) or not item[field].strip():
                raise ValueError(f"Published field is empty: {item['slug']}: {field}")
        if not isinstance(item["sources"], list) or not item["sources"]:
            raise ValueError(f"Published entry requires sources: {item['slug']}")
        for source in item["sources"]:
            if not isinstance(source, dict) or not source.get("url"):
                raise ValueError(f"Published source is incomplete: {item['slug']}")
        if not isinstance(item["seo"], dict) or not item["seo"]:
            raise ValueError(f"Published entry requires SEO fields: {item['slug']}")
        if item["diagram"] is not None and not isinstance(item["diagram"], dict):
            raise ValueError(f"Diagram must be an object or null: {item['slug']}")


def render_detail(
    item: dict[str, Any], previous: dict[str, Any] | None, next_item: dict[str, Any] | None
) -> str:
    """Reserve rendering for complete published items only.

    Task 2 supplies the shared HTML template. This guard makes it impossible for
    an identity-only record to become public in the meantime.
    """
    if not item.get("published"):
        raise ValueError(f"Item is not published: {item.get('slug', '<unknown>')}")
    validate_catalogue([item], expected_count=1)
    raise NotImplementedError("Detail rendering is implemented in Task 2")


def build(
    root: str | Path, catalogue: Iterable[dict[str, Any]], *, expected_count: int = 188
) -> list[Path]:
    """Validate the registry without generating public files before Task 2."""
    del root
    items = list(catalogue)
    validate_catalogue(items, expected_count=expected_count)
    return []
