# Core scraper — extracts rich brand signals from a given URL.
# Responsibilities:
#   - Fetch HTML from the URL using httpx
#   - Parse and extract: title, meta description, headings, body text,
#     nav link text, og:image, logo URL
#   - Return a structured dict passed to core/ai.py
#   - No HTTP routes, no DB — pure async function
#
# Functions:
#   - scrape_website(url: str) -> dict : returns scraped brand signals


# import httpx
# from bs4 import BeautifulSoup
# from urllib.parse import urljoin

# url = "https://dainwi.vercel.app/"

# req = httpx.get(url)
# soup = BeautifulSoup(req.text, "html.parser")

# urls = []

# for link in soup.find_all("a"):
#     href = link.get("href")
#     if href and href.startswith("http") and href not in urls:
#         urls.append(href)

# print(urls)


import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def _get_text(tag) -> str:
    return tag.get_text(strip=True) if tag else ""


async def scrape_website(url: str | "https://dainwi.vercel.app") -> dict:
    try:
        async with httpx.AsyncClient(
            timeout=15,
            follow_redirects=True,
            headers={"User-Agent": "BrandDNA-Bot/1.0"},
        ) as client:
            response = await client.get(str(url))
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        return {"url": str(url), "error": f"HTTP {e.response.status_code}"}
    except httpx.RequestError as e:
        return {"url": str(url), "error": str(e)}

    soup = BeautifulSoup(response.text, "html.parser")

    # --- Meta signals ---
    title = _get_text(soup.title)
    
    # Try both name and property attributes for meta description
    meta_desc_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "description"}) or soup.find("meta", attrs={"property": "og:description"})
    meta_desc = meta_desc_tag.get("content", "") if meta_desc_tag else ""
    
    og_image  = (soup.find("meta", attrs={"property": "og:image"}) or {}).get("content", "")
    og_title  = (soup.find("meta", attrs={"property": "og:title"}) or {}).get("content", "")

    if og_image and not og_image.startswith("http"):
        og_image = urljoin(str(url), og_image)

    # --- Headings (key brand messaging) ---
    headings = [
        tag.get_text(strip=True)
        for tag in soup.find_all(["h1", "h2", "h3"])
        if tag.get_text(strip=True)
    ][:15]  # limit to 15 most important headings

    # --- Navigation links (reveal brand positioning words) ---
    # Extract BEFORE decomposing nav/header
    nav_links = []
    navs = soup.find_all(["nav", "header"])
    for nav in navs:
        for a in nav.find_all("a"):
            text = a.get_text(strip=True)
            if text and text not in nav_links:
                nav_links.append(text)
    nav_links = nav_links[:15]

    # --- Logo URL guess ---
    # Extract BEFORE decomposing header/nav
    logo_url = ""
    for img in soup.find_all("img"):
        alt = (img.get("alt") or "").lower()
        src = (img.get("src") or "").lower()
        classes = " ".join(img.get("class") or []).lower()
        if "logo" in alt or "logo" in src or "logo" in classes:
            logo_url = urljoin(str(url), img.get("src", ""))
            break

    # If no logo found, check for a link containing an SVG logo or class 'logo'
    if not logo_url:
        logo_a = soup.find("a", class_=lambda c: c and "logo" in str(c).lower())
        if logo_a:
            img = logo_a.find("img")
            if img:
                logo_url = urljoin(str(url), img.get("src", ""))

    # --- Body text ---
    # Now that we've extracted nav links and logos, we can safely decompose
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    
    body_text = " ".join(soup.get_text(separator=" ").split())[:4000]

    print("url: ", url)
    print("title: ", title)
    print("og_title: ", og_title)
    print("meta_description: ", meta_desc)
    print("og_image: ", og_image)
    print("logo_url: ", logo_url)
    print("headings: ", headings)
    print("body_text: ", body_text)
    print("nav_links: ", nav_links)

    return {
        "url":          str(url),
        "title":        title,
        "og_title":     og_title,
        "meta_description": meta_desc,
        "og_image":     og_image,
        "logo_url":     logo_url,
        "headings":     headings,
        "body_text":    body_text,
        "nav_links":    nav_links,
    }
