import json
import vertexai
from vertexai.preview.generative_models import GenerativeModel, GenerationConfig

# -------------------------------------------------------------------
# Vertex AI initialization
# -------------------------------------------------------------------
# NOTE:
# - Project + region must match your GCP setup
# - Safe to keep this here for Cloud Run
vertexai.init(
    project="wekit-mvp",
    location="us-central1"
)

# Load Gemini Pro 2.5
model = GenerativeModel("gemini-2.5-pro")


# -------------------------------------------------------------------
# Core Career Mentor / Psychometric Engine
# -------------------------------------------------------------------
def run_career_mentor(
    age: int,
    interests: list[str],
    strengths_summary: str | None = None,
    values_summary: str | None = None,
    context: str = "India"
) -> dict:
    """
    AI-powered, explainable career mentoring engine for We-KIT.

    This function is:
    - Directional, not deterministic
    - Psychometrically inspired (not diagnostic)
    - Safe for youth, schools, NGOs, and CSR use
    - Designed for explainability and trust
    """

    prompt = f"""
You are an expert AI Career Mentor working with youth in {context}.

Your role:
- Help users explore possibilities, not make final decisions.
- Be encouraging, realistic, and culturally sensitive.
- Avoid labels, judgments, or claims of certainty.

User profile:
- Age: {age}
- Interests: {", ".join(interests)}
- Strengths summary: {strengths_summary or "Not provided"}
- Values / purpose summary: {values_summary or "Not provided"}

Your tasks:
1. Ask exactly 3 thoughtful diagnostic questions to deepen understanding.
2. Identify 2–3 possible career direction clusters that could fit the user.
3. Suggest practical next learning or exploration steps.

Rules:
- Do NOT say “this career is best for you”.
- Do NOT rank the user against others.
- Use exploratory language (“may suit”, “could align”, “worth exploring”).
- Assume diverse socioeconomic backgrounds.

Respond ONLY in valid JSON using this exact structure:

{{
  "diagnostic_questions": [
    "string",
    "string",
    "string"
  ],
  "career_clusters": [
    {{
      "name": "string",
      "why_it_fits": "string"
    }}
  ],
  "next_steps": [
    "string",
    "string",
    "string"
  ]
}}
"""

    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            temperature=0.4,
            max_output_tokens=600
        )
    )

    # Enforce strict JSON parsing for reliability
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        raise ValueError(
            "Gemini returned invalid JSON. "
            "This should be logged and retried or handled gracefully."
        )

