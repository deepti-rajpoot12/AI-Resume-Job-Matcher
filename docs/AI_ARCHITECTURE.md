# AI Architecture

## Prompt engineering

The application uses separate, versioned system prompts for resume analysis (`v2`) and career guidance (`v2`). Prompts define the role, allowed evidence, grounding rules, and structured-output requirement. Modify one task prompt at a time and retain validation tests.

## Context engineering

`app/prompts/context.py` assembles bounded context in deterministic priority order: candidate evidence, job requirements, skill gaps, retrieved knowledge, and task. System instructions are sent separately and have highest priority. Resume, job, retrieval-count, and retrieval-character limits avoid sending unbounded input.

## Grounding

Resume analysis may claim candidate facts only from resume evidence. Career guidance may claim candidate facts only from the validated analysis; Chroma knowledge supports learning recommendations only. Retrieved chunks retain skill, topic, and relevance metadata and are cleaned of duplicates before Gemini receives them.

## Safe changes

Do not place prompts in routes or frontend code. Update a prompt version when its behavior changes, preserve Pydantic schemas, and add a scenario to the prompt evaluation dataset before deploying.
