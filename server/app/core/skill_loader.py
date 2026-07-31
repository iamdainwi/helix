import os
import re

# We will cache the loaded skills in memory along with their mtime
_skills_cache: dict[str, tuple[float, str]] = {}

def load_skill(skill_name: str) -> str:
    """
    Loads a skill from the skills directory by name (e.g. 'senior-brand-strategist').
    Parses the YAML frontmatter and returns just the prompt body.
    Uses mtime-based caching so edits to .md files take effect without restarting.
    """
    # Path to the skills directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    skills_dir = os.path.join(base_dir, "skills")
    file_path = os.path.join(skills_dir, f"{skill_name}.md")

    if not os.path.exists(file_path):
        raise ValueError(f"Skill '{skill_name}' not found at {file_path}")

    current_mtime = os.path.getmtime(file_path)

    # Return cached version only if the file hasn't changed
    if skill_name in _skills_cache:
        cached_mtime, cached_body = _skills_cache[skill_name]
        if cached_mtime == current_mtime:
            return cached_body

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to extract frontmatter and body
    # Match ---, anything in between, ---, and then the rest of the file
    match = re.match(r"^---\n(.*?)\n---\n(.*)", content, re.DOTALL)
    if match:
        # frontmatter = match.group(1) # We could parse name/description here if needed
        body = match.group(2).strip()
    else:
        # Fallback if no frontmatter
        body = content.strip()

    _skills_cache[skill_name] = (current_mtime, body)
    return body
