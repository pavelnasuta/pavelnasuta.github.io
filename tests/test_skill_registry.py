from pathlib import Path
import unittest

from tools.build_skills import AGENT_STATES, load_registry, public_items, validate_registry


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_AGENTS = {"hermes", "claude-code", "codex", "opencode", "agents-md"}


class SkillRegistryTests(unittest.TestCase):
    def test_public_records_have_unique_safe_slugs_and_required_public_fields(self):
        items = load_registry(ROOT / "data/skills.json")
        validate_registry(items)
        visible = public_items(items)
        self.assertEqual(
            {item["slug"] for item in visible},
            {"book-summary", "adaptive-support-dialogue", "management-assistant"},
        )
        for item in visible:
            self.assertTrue(item["summary"])
            self.assertTrue(item["category"])
            self.assertTrue(item["tags"])
            self.assertTrue(item["page_url"])
            self.assertEqual(set(item["compatibility"]), EXPECTED_AGENTS)
            self.assertTrue(set(item["compatibility"].values()) <= AGENT_STATES)

    def test_non_public_records_cannot_expose_a_public_repository_url(self):
        items = load_registry(ROOT / "data/skills.json")
        validate_registry(items)
        for item in items:
            if item["visibility"] != "public":
                self.assertFalse(item["repository_url"])


if __name__ == "__main__":
    unittest.main()
