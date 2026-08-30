import unittest

from app.prompts.context import build_resume_analysis_context, clean_retrieved_context
from app.services.retrieval import RetrievedKnowledge


class PromptContextTests(unittest.TestCase):
    def test_resume_context_has_deterministic_sections(self):
        context = build_resume_analysis_context("Python developer", "Need Python")
        self.assertLess(context.index("## RESUME EVIDENCE"), context.index("## JOB REQUIREMENTS"))
        self.assertLess(context.index("## JOB REQUIREMENTS"), context.index("## TASK"))

    def test_retrieved_context_removes_duplicate_chunks(self):
        item = RetrievedKnowledge("Docker fundamentals", {"skill": "Docker"}, 0.2)
        context, count = clean_retrieved_context([item, item])
        self.assertEqual(count, 1)
        self.assertIn("Skill: Docker", context)


if __name__ == "__main__":
    unittest.main()
