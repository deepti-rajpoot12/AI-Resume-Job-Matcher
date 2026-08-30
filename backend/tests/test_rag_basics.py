import unittest

from pydantic import ValidationError

from app.models.career_guidance import CareerGuidanceRequest
from app.services.ingestion import chunk_text


class RagBasicsTests(unittest.TestCase):
    def test_chunk_text_preserves_all_words(self):
        chunks = chunk_text("one two three four five", chunk_size=3, overlap=1)
        self.assertEqual(chunks, ["one two three", "three four five"])

    def test_career_guidance_request_requires_job_description(self):
        payload = {"analysis": {"match_score": 50, "matching_skills": [], "missing_skills": [], "strengths": [], "improvement_suggestions": [], "interview_questions": []}, "job_description": ""}
        with self.assertRaises(ValidationError):
            CareerGuidanceRequest.model_validate(payload)


if __name__ == "__main__":
    unittest.main()
