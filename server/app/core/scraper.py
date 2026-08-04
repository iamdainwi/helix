import re
from collections import Counter
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

# Playwright is used as a JS-rendering fallback for SPA / React sites.
# We import lazily inside the function so startup doesn't fail if playwright
# isn't installed (it's only used in the fallback path).
_PLAYWRIGHT_AVAILABLE: bool | None = None

async def _fetch_with_playwright(url: str) -> str:
    """
    Launch a headless Chromium instance, navigate to `url`, wait for the
    network to settle, and return the fully-rendered HTML.
    """
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/138.0 Safari/537.36"
            )
        )
        try:
            await page.goto(url, wait_until="networkidle", timeout=30_000)
            html = await page.content()
        finally:
            await browser.close()


def _get_text(tag) -> str:
    return tag.get_text(" ", strip=True) if tag else ""


def _unique(items):
    seen = set()
    output = []

    for item in items:
        item = item.strip()
        if item and item not in seen:
            seen.add(item)
            output.append(item)

    return output


def _parse_color(color_str: str):
    color_str = color_str.strip().lower()
    if color_str.startswith('#'):
        h = color_str.lstrip('#')
        if len(h) == 3:
            h = ''.join(c + c for c in h)
        if len(h) in (6, 8):
            try:
                return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
            except ValueError:
                return None
    elif color_str.startswith('rgb'):
        nums = re.findall(r'\d+', color_str)
        if len(nums) >= 3:
            return (int(nums[0]), int(nums[1]), int(nums[2]))
    return None


def _is_distinct(new_color: str, accepted_colors: list[str], threshold: int = 2500) -> bool:
    new_rgb = _parse_color(new_color)
    if not new_rgb:
        return True # Can't parse, assume distinct
    
    for c in accepted_colors:
        c_rgb = _parse_color(c)
        if c_rgb:
            dist = sum((a - b) ** 2 for a, b in zip(new_rgb, c_rgb))
            if dist < threshold:
                return False
    return True


async def scrape_website(url: str) -> dict:
    """
    Scrapes a website and extracts structured brand signals.

    Returns:
    {
        url,
        title,
        description,
        language,
        canonical,
        favicon,
        theme_color,
        og_title,
        og_image,
        logo_url,
        headings,
        nav_links,
        cta_buttons,
        body_text,
        css_variables,
        color_palette,
        typography,
        font_sizes,
        font_weights,
        open_graph,
        twitter,
        social_links,
        json_ld
    }
    """

    try:
        html: str | None = None

        # --- First attempt: plain HTTP (fast, works for SSR/static sites) ---
        try:
            async with httpx.AsyncClient(
                timeout=20,
                follow_redirects=True,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/138.0 Safari/537.36"
                    )
                },
            ) as client:
                response = await client.get(str(url))
                response.raise_for_status()
                html = response.text
        except Exception:
            pass

        # --- Check if the page has enough content; if not, use Playwright ---
        _text_preview = BeautifulSoup(html or "", "html.parser").get_text(" ", strip=True) if html else ""
        if len(" ".join(_text_preview.split())) < 300:
            # JS-heavy SPA detected — fall back to headless Chromium
            html = await _fetch_with_playwright(str(url))

        soup = BeautifulSoup(html, "html.parser")

        # Re-open an httpx client for CSS file fetching
        async with httpx.AsyncClient(
            timeout=15,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/138.0 Safari/537.36"
                )
            },
        ) as client:

            ############################################################
            # BASIC META
            ############################################################

            title = _get_text(soup.title)

            meta_description = ""

            for selector in [
                {"name": "description"},
                {"property": "description"},
                {"property": "og:description"},
            ]:
                tag = soup.find("meta", attrs=selector)
                if tag:
                    meta_description = tag.get("content", "")
                    break

            og_title = (
                soup.find("meta", attrs={"property": "og:title"}) or {}
            ).get("content", "")

            og_image = (
                soup.find("meta", attrs={"property": "og:image"}) or {}
            ).get("content", "")

            if og_image:
                og_image = urljoin(str(url), og_image)

            ############################################################
            # HTML METADATA
            ############################################################

            language = ""

            if soup.html:
                language = soup.html.get("lang", "")

            canonical = ""

            canonical_tag = soup.find("link", rel="canonical")

            if canonical_tag:
                canonical = canonical_tag.get("href", "")

            favicon = ""

            for rel in [
                "icon",
                "shortcut icon",
                "apple-touch-icon",
            ]:
                tag = soup.find(
                    "link",
                    rel=lambda x: x and rel in x.lower(),
                )

                if tag:
                    favicon = urljoin(
                        str(url),
                        tag.get("href", ""),
                    )
                    break

            theme_color = ""

            tag = soup.find(
                "meta",
                attrs={"name": "theme-color"},
            )

            if tag:
                theme_color = tag.get("content", "")

            ############################################################
            # HEADINGS
            ############################################################

            headings = _unique(
                [
                    _get_text(tag)
                    for tag in soup.find_all(
                        ["h1", "h2", "h3"]
                    )
                ]
            )[:20]

            ############################################################
            # NAVIGATION
            ############################################################

            nav_links = []

            for nav in soup.find_all(["nav", "header"]):
                for a in nav.find_all("a"):
                    text = _get_text(a)

                    if text:
                        nav_links.append(text)

            nav_links = _unique(nav_links)[:20]

            ############################################################
            # CTA BUTTONS
            ############################################################

            cta_buttons = []

            for tag in soup.find_all(["button", "a"]):
                text = _get_text(tag)

                if (
                    text
                    and len(text) <= 40
                ):
                    cta_buttons.append(text)

            cta_buttons = _unique(cta_buttons)[:20]

            ############################################################
            # LOGO
            ############################################################

            logo_url = ""

            selectors = [
                'img[alt*="logo" i]',
                'img[src*="logo" i]',
                ".logo img",
                "#logo img",
                "header img",
            ]

            for selector in selectors:
                node = soup.select_one(selector)

                if node:
                    src = node.get("src")

                    if src:
                        logo_url = urljoin(
                            str(url),
                            src,
                        )
                        break

            ############################################################
            # SOCIAL LINKS
            ############################################################

            social_links = {}

            for a in soup.find_all(
                "a",
                href=True,
            ):
                href = a["href"]

                lower = href.lower()

                for site in [
                    "linkedin",
                    "github",
                    "twitter",
                    "instagram",
                    "facebook",
                    "youtube",
                    "discord",
                    "dribbble",
                    "behance",
                ]:
                    if site in lower:
                        social_links[site] = href

            ############################################################
            # OPEN GRAPH
            ############################################################

            open_graph = {}

            for tag in soup.find_all(
                "meta",
                attrs={"property": True},
            ):
                prop = tag["property"]

                if prop.startswith("og:"):
                    open_graph[prop] = tag.get(
                        "content",
                        "",
                    )

            ############################################################
            # TWITTER
            ############################################################

            twitter = {}

            for tag in soup.find_all(
                "meta",
                attrs={"name": True},
            ):
                name = tag["name"]

                if name.startswith("twitter:"):
                    twitter[name] = tag.get(
                        "content",
                        "",
                    )

            ############################################################
            # JSON LD
            ############################################################

            json_ld = []

            for script in soup.find_all(
                "script",
                type="application/ld+json",
            ):
                if script.string:
                    json_ld.append(script.string)

            ############################################################
            # CSS FILES
            ############################################################

            css_urls = []

            for link in soup.find_all(
                "link",
                rel=lambda x: x and "stylesheet" in x.lower(),
            ):
                href = link.get("href")

                if href:
                    css_urls.append(
                        urljoin(
                            str(url),
                            href,
                        )
                    )

            css_text = ""

            for css_url in css_urls:
                try:
                    css_response = await client.get(css_url)

                    if css_response.status_code == 200:
                        css_text += (
                            "\n"
                            + css_response.text
                        )
                except Exception:
                    pass

            ############################################################
            # CSS VARIABLES
            ############################################################

            css_variables = dict(
                re.findall(
                    r"(--[\w-]+)\s*:\s*([^;]+);",
                    css_text,
                    re.IGNORECASE,
                )
            )

            ############################################################
            # COLORS
            ############################################################

            # Prioritize CSS variables that might be brand colors
            brand_css_colors = []
            for var_name, var_value in css_variables.items():
                name_lower = var_name.lower()
                if any(kw in name_lower for kw in ["primary", "brand", "accent", "secondary", "background", "bg", "text", "foreground"]):
                    brand_css_colors.append(var_value)

            color_regex = re.compile(
                r"""
                \#[0-9a-fA-F]{3,8}
                |
                rgb[a]?\([^)]+\)
                |
                hsl[a]?\([^)]+\)
                |
                oklch\([^)]+\)
                """,
                re.VERBOSE | re.IGNORECASE,
            )

            colors = Counter(
                color_regex.findall(css_text)
            )

            # Combine prioritized CSS colors and most common raw colors
            candidate_colors = brand_css_colors + [
                color
                for color, _
                in colors.most_common(50)
            ]

            # Deduplicate visually similar colors
            color_palette = []
            for color in candidate_colors:
                # Basic string deduplication
                if color in color_palette:
                    continue
                # Semantic deduplication based on Euclidean distance
                if _is_distinct(color, color_palette, threshold=2000):
                    color_palette.append(color)
                
                if len(color_palette) >= 12:
                    break

            ############################################################
            # TYPOGRAPHY
            ############################################################

            GENERIC_FAMILIES = {
                "serif", "sans-serif", "monospace", "cursive",
                "fantasy", "system-ui", "inherit", "initial",
                "unset", "ui-sans-serif", "ui-serif",
                "-apple-system", "blinkmacsystemfont",
            }

            font_regex = re.compile(
                r"font-family\s*:\s*([^;]+);",
                re.IGNORECASE,
            )

            fonts = Counter()

            for family in font_regex.findall(
                css_text
            ):
                for font in family.split(","):
                    font = (
                        font.strip()
                        .strip("'")
                        .strip('"')
                    )

                    if font and font.lower() not in GENERIC_FAMILIES:
                        fonts[font] += 1

            typography = [
                font
                for font, _
                in fonts.most_common(10)
            ]

            ############################################################
            # FONT SIZES
            ############################################################

            font_sizes = Counter(
                re.findall(
                    r"font-size\s*:\s*([^;]+);",
                    css_text,
                    re.IGNORECASE,
                )
            )

            ############################################################
            # FONT WEIGHTS
            ############################################################

            font_weights = Counter(
                re.findall(
                    r"font-weight\s*:\s*([^;]+);",
                    css_text,
                    re.IGNORECASE,
                )
            )

            ############################################################
            # BODY TEXT
            ############################################################

            for tag in soup(
                [
                    "script",
                    "style",
                    "noscript",
                    "footer",
                    "header",
                    "nav",
                    "aside",
                ]
            ):
                tag.decompose()

            body_text = " ".join(
                soup.get_text(
                    separator=" "
                ).split()
            )[:5000]

            if len(body_text) < 200:
                raise ValueError("Site appears to be JS-rendered (or has extremely little text). HTML body text is under 200 characters. We need a headless browser to scrape this site.")

            ############################################################
            # RETURN
            ############################################################

            return {
                "url": str(url),
                "title": title,
                "meta_description": meta_description,
                "language": language,
                "canonical": canonical,
                "favicon": favicon,
                "theme_color": theme_color,
                "og_title": og_title,
                "og_image": og_image,
                "logo_url": logo_url,
                "headings": headings,
                "nav_links": nav_links,
                "cta_buttons": cta_buttons,
                "body_text": body_text,
                "css_variables": css_variables,
                "color_palette": color_palette,
                "typography": typography,
                "font_sizes": dict(font_sizes),
                "font_weights": dict(font_weights),
                "open_graph": open_graph,
                "twitter": twitter,
                "social_links": social_links,
                "json_ld": json_ld,
            }

    except httpx.HTTPStatusError as e:
        return {
            "url": str(url),
            "error": f"HTTP {e.response.status_code}",
        }

    except httpx.RequestError as e:
        return {
            "url": str(url),
            "error": str(e),
        }

    except Exception as e:
        return {
            "url": str(url),
            "error": str(e),
        }