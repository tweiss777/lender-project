"""
PDF Parser Service
==================
Sends a lender guidelines PDF to the Claude API and extracts structured
policy data. Returns a LenderPreview for user confirmation before saving.
"""

import base64
import json
import os

import httpx

from app.Schemas.lender_policy_preview import LenderPreview

ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-4-20250514"

EXTRACTION_PROMPT = """
You are a financial document parser. Extract lender credit policy information from this PDF.

Return ONLY a valid JSON object — no explanation, no markdown, no code fences.

The JSON must follow this exact structure:
{
  "lender_name": "string — the name of the lending institution",
  "programs": [
    {
      "program_name": "string — name of this specific program or tier",
      "min_loan_amount": number or null,
      "max_loan_amount": number or null,
      "min_term_months": number or null,
      "max_term_months": number or null,
      "min_fico": number or null,
      "min_paynet_score": number or null,
      "min_years_in_business": number or null,
      "min_revenue": number or null,
      "max_equipment_age_years": number or null,
      "equipment_restrictions": ["list of restricted equipment types, e.g. Aircraft, ATM"],
      "allowed_states": ["two-letter state codes if the lender only operates in specific states"],
      "excluded_states": ["two-letter state codes the lender explicitly will NOT operate in"],
      "allowed_industries": ["industries if the lender only accepts specific ones"],
      "excluded_industries": ["industries the lender explicitly excludes"],
      "no_bankruptcy": true/false/null — true if lender accepts NO prior bankruptcies,
      "min_years_since_bankruptcy": number or null — minimum years since discharge,
      "allows_judgments": true/false/null — false if lender rejects applicants with judgments,
      "allows_liens": true/false/null — false if lender rejects applicants with tax liens,
      "requires_us_citizen": true/false/null
    }
  ]
}

Rules:
- If a lender has multiple tiers or programs (e.g. Tier 1/2/3 or A/B/C Rate), create a separate object in "programs" for each one.
- Use null for any field not mentioned in the document.
- Use empty arrays [] for list fields with no relevant data.
- For dollar amounts, use raw numbers without commas (e.g. 75000 not 75,000).
- For states, use two-letter abbreviations (e.g. "CA" not "California").
- no_bankruptcy and min_years_since_bankruptcy are mutually exclusive — use one or the other, not both.
""".strip()


def parse_lender_pdf(pdf_bytes: bytes) -> LenderPreview:
    """
    Send a PDF to the Claude API and return a structured LenderPreview.

    Raises:
        ValueError: if the API response cannot be parsed as valid JSON
        httpx.HTTPError: if the API call fails
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")

    pdf_b64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    payload = {
        "model": MODEL,
        "max_tokens": 4096,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": pdf_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": EXTRACTION_PROMPT,
                    },
                ],
            }
        ],
    }

    response = httpx.post(
        ANTHROPIC_API_URL,
        json=payload,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        timeout=60.0,
    )
    response.raise_for_status()

    content = response.json()["content"][0]["text"].strip()

    # Strip markdown code fences if the model includes them despite instructions
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Claude returned invalid JSON: {e}\n\nRaw response:\n{content}")

    return LenderPreview(**data)
