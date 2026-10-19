import json
from pathlib import Path
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
        self.assertEqual(build(ROOT, [item], expected_count=1), [])


if __name__ == "__main__":
    unittest.main()
