# Core AI — calls Ollama Cloud API to generate structured Brand DNA.
# Responsibilities:
#   - Accept scraped website data as input
#   - Construct a rich structured prompt for the LLM
#   - Call Ollama Cloud (https://ollama.com/api/chat) with Bearer auth
#   - Parse and return structured brand DNA dict safely
#   - No HTTP routes, no DB — pure async function
#
# Functions:
#   - extract_brand_dna(scraped_data: dict) -> dict
#       Returns: {
#           "brand_name"        : str,
#           "tagline"           : str,
#           "tone_of_voice"     : str,
#           "brand_personality" : list[str],   # e.g. ["bold", "trustworthy"]
#           "color_palette"     : list[str],   # hex codes or descriptive
#           "typography"        : str,
#           "audience"          : str,
#           "values"            : list[str],
#           "design_style"      : str,         # e.g. "minimalist", "vibrant"
#           "logo_url"          : str,
#       }

import httpx
import json
import re
from fastapi import HTTPException
from app.config import settings
from app.core.skill_loader import load_skill

def _extract_json(raw: str) -> dict:
    """
    Safely parse JSON from the model response.
    Handles cases where the model wraps output in markdown fences.
    """
    cleaned = re.sub(r"```(?:json)?", "", raw).strip()
    match = re.search(r"\{.*\}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in model response")
    return json.loads(match.group())

async def extract_brand_dna_ollama(scraped_data: dict) -> dict:
    if not settings.OLLAMA_API_KEY:
        raise HTTPException(503, "OLLAMA_API_KEY is not configured")

    # Strip noise before building prompt
    clean_data = {
        "title": scraped_data.get("title"),
        "meta_description": scraped_data.get("meta_description"),
        "og_title": scraped_data.get("og_title"),
        "headings": scraped_data.get("headings", [])[:10],
        "body_text": scraped_data.get("body_text", "")[:2000],
        "color_palette": scraped_data.get("color_palette", [])[:10],
        "css_variables": scraped_data.get("css_variables", {}),
        "typography": scraped_data.get("typography", [])[:5],
        "nav_links": scraped_data.get("nav_links", []),
        "cta_buttons": scraped_data.get("cta_buttons", []),
        "json_ld": scraped_data.get("json_ld"),
        "social_links": scraped_data.get("social_links"),
    }

    template = load_skill("senior-brand-strategist")
    prompt = template.format(data=json.dumps(clean_data, indent=2))

    payload = {
        "model": settings.OLLAMA_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False,
    }

    headers = {
        "Authorization": f"Bearer {settings.OLLAMA_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                f"{settings.OLLAMA_CLOUD_HOST}/api/chat",
                json=payload,
                headers=headers,
            )
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(e.response.text)
        raise HTTPException(502, f"Ollama Cloud returned an error: {e.response.status_code}")
    except httpx.RequestError as e:
        raise HTTPException(502, f"Could not reach Ollama Cloud: {str(e)}")

    raw = response.json().get("message", {}).get("content", "")
    if not raw:
        raise HTTPException(502, "Ollama Cloud returned an empty response")

    try:
        return _extract_json(raw)
    except (ValueError, json.JSONDecodeError) as e:
        raise HTTPException(500, f"AI returned invalid JSON: {str(e)}")


async def extract_brand_dna_gemini(scraped_data: dict) -> dict:
    if not settings.GEMINI_API_KEY:
        raise HTTPException(503, "GEMINI_API_KEY is not configured")

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        raise HTTPException(500, "Google GenAI SDK is not installed")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)

    # Strip noise before building prompt
    clean_data = {
        "title": scraped_data.get("title"),
        "meta_description": scraped_data.get("meta_description"),
        "og_title": scraped_data.get("og_title"),
        "headings": scraped_data.get("headings", [])[:10],
        "body_text": scraped_data.get("body_text", "")[:2000],
        "color_palette": scraped_data.get("color_palette", [])[:10],
        "css_variables": scraped_data.get("css_variables", {}),
        "typography": scraped_data.get("typography", [])[:5],
        "nav_links": scraped_data.get("nav_links", []),
        "cta_buttons": scraped_data.get("cta_buttons", []),
        "json_ld": scraped_data.get("json_ld"),
        "social_links": scraped_data.get("social_links"),
    }

    template = load_skill("senior-brand-strategist")
    prompt = template.format(data=json.dumps(clean_data, indent=2))

    try:
        response = await client.aio.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
    except Exception as e:
        raise HTTPException(502, f"Gemini API returned an error: {str(e)}")

    raw = response.text
    if not raw:
        raise HTTPException(502, "Gemini returned an empty response")

    try:
        return _extract_json(raw)
    except (ValueError, json.JSONDecodeError) as e:
        raise HTTPException(500, f"AI returned invalid JSON: {str(e)}")

# Make Gemini the default AI provider
extract_brand_dna = extract_brand_dna_gemini
