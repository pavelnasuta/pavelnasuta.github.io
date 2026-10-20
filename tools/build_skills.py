"""Validate the private registry that drives the public Skill Hub."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SAFE_SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
AGENT_STATES = frozenset({"verified", "compatible", "planned", "not-applicable"})
AGENTS = frozenset({"hermes", "claude-code", "codex", "opencode", "agents-md"})
VISIBILITIES = frozenset({"public", "private-pilot", "withheld"})
STATUSES = frozenset({"draft", "reviewed", "released", "private-pilot", "withheld"})
SOURCE_STATUSES = frozenset({"not-started", "sanitizing", "review-ready", "published"})
REQUIRED_FIELDS = frozenset(
    {
        "slug",
        "name",
        "summary",
        "category",
        "tags",
        "status",
        "visibility",
        "source_status",
        "compatibility",
        "updated",
        "version",
        "license",
        "repository_url",
        "page_url",
        "privacy_review",
        "release_notes",
        "release_priority",
    }
)


def load_registry(path: Path) -> list[dict[str, Any]]:
    """Load a registry document with an ordered `items` array."""
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or not isinstance(document.get("items"), list):
        raise ValueError("Skill registry must be a JSON object with an items array")
    return document["items"]


def _require_text(item: dict[str, Any], field: str) -> None:
    if not isinstance(item[field], str) or not item[field].strip():
        raise ValueError(f"Skill field must be non-empty text: {item['slug']}: {field}")


def validate_registry(items: list[dict[str, Any]]) -> None:
    """Reject malformed public records before they can reach the site."""
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Skill records must be JSON objects")
        missing = REQUIRED_FIELDS - item.keys()
        if missing:
            raise ValueError(f"Incomplete skill record: {item.get('slug', '<unknown>')}: {sorted(missing)}")
        slug = item["slug"]
        if not isinstance(slug, str) or not SAFE_SLUG.fullmatch(slug):
            raise ValueError(f"Invalid skill slug: {slug!r}")
        if slug in seen:
            raise ValueError(f"Duplicate skill slug: {slug}")
        seen.add(slug)
        for field in ("name", "summary", "category", "status", "visibility", "source_status", "updated", "version", "license", "privacy_review", "release_notes"):
            _require_text(item, field)
        if item["status"] not in STATUSES:
            raise ValueError(f"Unknown status: {slug}: {item['status']}")
        if item["visibility"] not in VISIBILITIES:
            raise ValueError(f"Unknown visibility: {slug}: {item['visibility']}")
        if item["source_status"] not in SOURCE_STATUSES:
            raise ValueError(f"Unknown source status: {slug}: {item['source_status']}")
        if not isinstance(item["tags"], list) or not item["tags"] or not all(isinstance(tag, str) and tag.strip() for tag in item["tags"]):
            raise ValueError(f"Skill requires non-empty tags: {slug}")
        if not isinstance(item["release_priority"], int) or item["release_priority"] < 1:
            raise ValueError(f"Skill requires positive release priority: {slug}")
        if not isinstance(item["compatibility"], dict) or set(item["compatibility"]) != AGENTS:
            raise ValueError(f"Skill requires a complete compatibility map: {slug}")
        if not set(item["compatibility"].values()) <= AGENT_STATES:
            raise ValueError(f"Skill compatibility contains an invalid state: {slug}")
        for field in ("repository_url", "page_url"):
            if not isinstance(item[field], str):
                raise ValueError(f"Skill URL must be text: {slug}: {field}")
        if item["visibility"] == "public":
            if not item["page_url"]:
                raise ValueError(f"Public skill has no local page: {slug}")
            if item["status"] not in {"released", "private-pilot"}:
                raise ValueError(f"Public skill has an invalid publication status: {slug}")
        else:
            if item["repository_url"] or item["page_url"]:
                raise ValueError(f"Non-public skill exposes a URL: {slug}")


def public_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return the records allowed to appear in the public catalogue."""
    return [item for item in items if item["visibility"] == "public" and item["page_url"]]


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate the Skill Hub registry")
    parser.add_argument("--registry", required=True, type=Path)
    args = parser.parse_args()
    items = load_registry(args.registry)
    validate_registry(items)
    print(json.dumps({"validated": len(items), "public": len(public_items(items))}, ensure_ascii=False))


if __name__ == "__main__":
    main()
