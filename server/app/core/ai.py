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

def _compress_for_prompt(scraped_data: dict) -> dict:
    """
    Aggressively compress scraped website data to fit within LLM context limits.
    A raw scrape can contain thousands of CSS variables and megabytes of text.
    We reduce it to a focused, dense signal that still contains all brand-relevant information.
    """
    # --- CSS Variables: keep only semantically meaningful brand tokens ---
    BRAND_KEYWORDS = {
        "primary", "secondary", "accent", "brand", "background", "bg",
        "foreground", "fg", "text", "heading", "surface", "muted",
        "card", "border", "ring", "link", "font", "radius",
    }
    raw_vars = scraped_data.get("css_variables", {})
    brand_vars = {
        k: v for k, v in raw_vars.items()
        if any(kw in k.lower() for kw in BRAND_KEYWORDS)
    }
    # Further limit to top 30 most relevant, keeping the dict small
    brand_vars = dict(list(brand_vars.items())[:30])

    # --- Body text: first 800 chars is enough for tone/audience analysis ---
    body_text = scraped_data.get("body_text", "")
    # Collapse whitespace aggressively
    body_text = " ".join(body_text.split())[:800]

    # --- Colors: max 8 distinct values ---
    colors = scraped_data.get("color_palette", [])[:8]

    # --- Typography: max 4 font families ---
    typography = scraped_data.get("typography", [])[:4]

    # --- JSON-LD: strip raw text, keep only @type and key name fields ---
    raw_ld = scraped_data.get("json_ld") or []
    json_ld_summary = []
    for item in raw_ld[:2]:  # at most 2 structured data blocks
        try:
            parsed = json.loads(item) if isinstance(item, str) else item
            summary = {k: parsed[k] for k in ("@type", "name", "description") if k in parsed}
            if summary:
                json_ld_summary.append(summary)
        except Exception:
            pass

    return {
        "title": (scraped_data.get("title") or "")[:120],
        "meta_description": (scraped_data.get("meta_description") or "")[:200],
        "og_title": (scraped_data.get("og_title") or "")[:120],
        "headings": scraped_data.get("headings", [])[:8],
        "body_text": body_text,
        "color_palette": colors,
        "css_variables": brand_vars,
        "typography": typography,
        "nav_links": scraped_data.get("nav_links", [])[:10],
        "cta_buttons": scraped_data.get("cta_buttons", [])[:8],
        "social_links": scraped_data.get("social_links") or {},
        "json_ld": json_ld_summary,
    }


async def extract_brand_dna_ollama(scraped_data: dict) -> dict:
    if not settings.OLLAMA_API_KEY:
        raise HTTPException(503, "OLLAMA_API_KEY is not configured")

    clean_data = _compress_for_prompt(scraped_data)
    template = load_skill("senior-brand-strategist")
    prompt = template.format(data=json.dumps(clean_data, indent=2, ensure_ascii=False))

    # Safety check — log if prompt is still large
    approx_tokens = len(prompt) // 4
    print(f"[AI] Ollama prompt ~{approx_tokens} tokens")


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
        error_body = e.response.text
        print(f"[Ollama Cloud] {e.response.status_code}: {error_body}")
        raise HTTPException(502, f"Ollama Cloud error ({e.response.status_code}): {error_body[:300]}")
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
    except ImportError:
        raise HTTPException(500, "Google GenAI SDK is not installed")

    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    clean_data = _compress_for_prompt(scraped_data)
    template = load_skill("senior-brand-strategist")
    prompt = template.format(data=json.dumps(clean_data, indent=2, ensure_ascii=False))

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

# Make Ollama the default AI provider
extract_brand_dna = extract_brand_dna_ollama
