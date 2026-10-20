from copy import deepcopy
import json
from pathlib import Path
import tempfile
import unittest

from tools.build_biases import (
    DETAIL_CATEGORIES,
    build,
    load_catalogue,
    render_detail,
    validate_catalogue,
)


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "content" / "biases" / "catalogue.json"
IDENTITY_FIELDS = {
    "slug",
    "russian_name",
    "english_name",
    "catalogue_category",
    "detail_category",
    "problem",
    "published",
}
EDITORIAL_FIELDS = {
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


class BiasesCatalogueTests(unittest.TestCase):
    def test_catalogue_has_exactly_188_unique_identities(self):
        items = json.loads(CATALOGUE.read_text(encoding="utf-8"))["items"]

        self.assertEqual(len(items), 188)
        self.assertEqual(len({item["slug"] for item in items}), 188)
        for item in items:
            with self.subTest(slug=item["slug"]):
                self.assertTrue(IDENTITY_FIELDS <= item.keys())
                self.assertTrue(item["slug"])
                self.assertTrue(item["russian_name"])
                self.assertTrue(item["english_name"])
                self.assertIsInstance(item["published"], bool)

    def test_only_published_items_require_complete_editorial_content(self):
        items = load_catalogue(CATALOGUE)
        validate_catalogue(items)

        published_items = [item for item in items if item["published"]]
        self.assertEqual(
            {item["slug"] for item in published_items},
            {"confirmation-bias", "anchoring"},
        )
        for item in published_items:
            with self.subTest(slug=item["slug"]):
                self.assertTrue(EDITORIAL_FIELDS <= item.keys())
                self.assertIn(item["detail_category"], DETAIL_CATEGORIES)
                self.assertTrue(item["sources"])
                self.assertTrue(item["seo"])

    def test_unpublished_identity_can_omit_editorial_fields(self):
        item = {
            "slug": "identity-only",
            "russian_name": "Только идентичность",
            "english_name": "Identity only",
            "catalogue_category": "Информация",
            "detail_category": "Когда информации слишком много",
            "problem": "Too Much Information",
            "published": False,
        }

        self.assertIsNone(validate_catalogue([item], expected_count=1))

    def test_published_identity_requires_complete_editorial_content(self):
        item = {
            "slug": "incomplete-published",
            "russian_name": "Неполная публикация",
            "english_name": "Incomplete published item",
            "catalogue_category": "Смысл",
            "detail_category": "Когда не хватает смысла",
            "problem": "What Should We Remember?",
            "published": True,
        }

        with self.assertRaisesRegex(ValueError, "Incomplete published entry"):
            validate_catalogue([item], expected_count=1)

    def test_published_source_requires_non_empty_string_url_and_citation(self):
        item = next(item for item in load_catalogue(CATALOGUE) if item["published"])

        for field, invalid_value in (
            ("url", ""),
            ("url", 42),
            ("citation", ""),
            ("citation", 42),
        ):
            with self.subTest(field=field, invalid_value=invalid_value):
                invalid_item = json.loads(json.dumps(item))
                invalid_item["sources"][0][field] = invalid_value

                with self.assertRaisesRegex(ValueError, "Published source is incomplete"):
                    validate_catalogue([invalid_item], expected_count=1)

    def test_published_seo_requires_non_empty_string_title_and_description(self):
        item = next(item for item in load_catalogue(CATALOGUE) if item["published"])

        for field, invalid_value in (
            ("title", ""),
            ("title", 42),
            ("description", ""),
            ("description", 42),
        ):
            with self.subTest(field=field, invalid_value=invalid_value):
                invalid_item = json.loads(json.dumps(item))
                invalid_item["seo"][field] = invalid_value

                with self.assertRaisesRegex(ValueError, "Published entry requires SEO fields"):
                    validate_catalogue([invalid_item], expected_count=1)

    def test_unpublished_identity_cannot_be_rendered_or_built(self):
        item = {
            "slug": "identity-only",
            "russian_name": "Только идентичность",
            "english_name": "Identity only",
            "catalogue_category": "Информация",
            "detail_category": "Когда информации слишком много",
            "problem": "Too Much Information",
            "published": False,
        }

        with self.assertRaisesRegex(ValueError, "not published"):
            render_detail(item, None, None)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            built = build(root, [item], expected_count=1)

            self.assertEqual(built, [root / "biases" / "index.html"])
            self.assertTrue((root / "biases" / "index.html").is_file())

    def test_build_removes_stale_generated_routes_but_preserves_other_files(self):
        published = deepcopy(
            next(item for item in load_catalogue(CATALOGUE) if item["published"])
        )
        unpublished = deepcopy(published)
        unpublished["published"] = False

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build(root, [published], expected_count=1)
            stale_route = root / "biases" / "old-generated" / "index.html"
            stale_route.parent.mkdir(parents=True)
            stale_route.write_text("obsolete generated page", encoding="utf-8")
            preserved = stale_route.parent / "notes.txt"
            preserved.write_text("do not remove", encoding="utf-8")

            built = build(root, [unpublished], expected_count=1)

            self.assertEqual(built, [root / "biases" / "index.html"])
            self.assertFalse((root / "biases" / published["slug"] / "index.html").exists())
            self.assertFalse(stale_route.exists())
            self.assertEqual(preserved.read_text(encoding="utf-8"), "do not remove")
            self.assertEqual(
                (root / "biases" / "index.html").read_text(encoding="utf-8").count(
                    '<a class="bias-row"'
                ),
                0,
            )

    def test_slug_must_be_a_safe_single_path_segment(self):
        base = {
            "russian_name": "Только идентичность",
            "english_name": "Identity only",
            "catalogue_category": "Информация",
            "detail_category": "Когда информации слишком много",
            "problem": "Too Much Information",
            "published": False,
        }

        for slug in ("../escape", "nested/path", "two--hyphens", "-leading", "trailing-", "UPPER"):
            with self.subTest(slug=slug):
                item = {**base, "slug": slug}

                with self.assertRaisesRegex(ValueError, "Invalid slug"):
                    validate_catalogue([item], expected_count=1)

    def test_renderer_escapes_dynamic_href_html_and_inline_json_data(self):
        item = deepcopy(next(item for item in load_catalogue(CATALOGUE) if item["published"]))
        attack = '</script><script>alert("injected")</script>'
        item["lede"] = attack
        item["sources"][0]["url"] = 'https://example.invalid/?q=\"><img src=x onerror=alert(1)>'

        page = render_detail(item, None, None)

        self.assertNotIn(attack, page)
        self.assertIn(
            'href="https://example.invalid/?q=&quot;&gt;&lt;img src=x onerror=alert(1)&gt;"',
            page,
        )
        structured_data = page.split('<script type="application/ld+json">', 1)[1].split(
            "</script>", 1
        )[0]
        self.assertNotIn("<", structured_data)
        self.assertEqual(json.loads(structured_data)["description"], attack)

    def test_random_routes_exclude_the_current_slug_and_are_deduplicated(self):
        current = deepcopy(next(item for item in load_catalogue(CATALOGUE) if item["published"]))
        other = deepcopy(current)
        other["slug"] = "other-bias"
        other["russian_name"] = "Другое искажение"

        page = render_detail(current, other, other)

        routes = json.loads(page.split("const routes=", 1)[1].split(";random.addEventListener", 1)[0])
        self.assertEqual(routes, ["../other-bias/index.html"])


if __name__ == "__main__":
    unittest.main()
