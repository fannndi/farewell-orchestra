"""
auto-load-skills.py — Auto-load critical skills AND persona at session start.
Generates compact context files for performance.
"""

import os, sys, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
SKILLS_DIR = ROOT / ".opencode" / "skills"
AGENTS_DIR = ROOT / ".opencode" / "agents"


def get_agent_skills(agent_name):
    """Get skills listed in agent frontmatter."""
    agent_file = AGENTS_DIR / f"{agent_name}.md"
    if not agent_file.exists():
        return []
    content = agent_file.read_text(encoding="utf-8")
    match = re.search(r"skills:\s*\[(.*?)\]", content)
    if match:
        return [s.strip() for s in match.group(1).split(",")]
    return []


def load_skill_content(skill_name):
    """Load skill content from disk."""
    skill_file = SKILLS_DIR / skill_name / "SKILL.md"
    if not skill_file.exists():
        return None
    return skill_file.read_text(encoding="utf-8")


def load_persona_content(agent_name):
    """Load persona content from agent .md file."""
    agent_file = AGENTS_DIR / f"{agent_name}.md"
    if not agent_file.exists():
        return None
    return agent_file.read_text(encoding="utf-8")


def extract_key_rules(content, max_lines=60):
    """Extract key rules from content, code-fence AND table safe.

    Caps at max_lines (default 60), then guards against cutting mid-fence:
    drops a trailing unterminated fence, and truncates at the last even
    fence boundary if the slice has an odd number of fences.
    Table-safe: a slice ending inside a markdown table leaves an incomplete
    table (rows with no trailing section) — drop the whole truncated table.
    """
    lines = [ln for ln in content.split("\n") if ln.strip() and not ln.startswith("#")]
    lines = lines[:max_lines]
    # Drop trailing unterminated fence
    if lines and lines[-1].lstrip().startswith("```"):
        lines.pop()
    # Odd fence count → slice at the last even boundary
    fences = [i for i, ln in enumerate(lines) if ln.lstrip().startswith("```")]
    if len(fences) % 2 == 1:
        lines = lines[: fences[-1]]
    # Table-safe: slice ended inside a table → scan back to the first table line
    # (header/separator/rows all start with "|"). Only drop if the table is
    # INCOMPLETE (no header separator `|---` in the scanned-back block). A
    # complete table ending exactly at the boundary is kept.
    if lines and lines[-1].lstrip().startswith("|"):
        i = len(lines) - 1
        while i >= 0 and lines[i].lstrip().startswith("|"):
            i -= 1
        table = lines[i + 1 :]
        if not any(re.search(r"^[\s|:-]+$", ln) and "-" in ln for ln in table):
            lines = lines[: i + 1]
    return "\n".join(lines)


def generate_skill_context(agent_name):
    """Generate compact skill context for an agent."""
    skills = get_agent_skills(agent_name)
    context_parts = []

    for skill_name in skills:
        content = load_skill_content(skill_name)
        if content:
            # Key rules up to 60 lines, fence-safe (no unterminated ```)
            key_content = extract_key_rules(content, max_lines=60)
            context_parts.append(f"=== {skill_name} ===\n{key_content}")

    return "\n\n".join(context_parts)


def generate_persona_context(agent_name):
    """Generate persona context — full body, frontmatter stripped.

    Safety rules (## Rules) sit near the END of every agent file, so a raw
    line cap drops them. Files are 77-78 lines: keep the full body.
    Only truncate oversized personas (> 120 lines).
    """
    content = load_persona_content(agent_name)
    if not content:
        return ""
    lines = content.split("\n")
    # Strip YAML frontmatter block (--- ... ---)
    if lines and lines[0].strip() == "---":
        close = next(
            (i for i in range(1, len(lines)) if lines[i].strip() == "---"), None
        )
        if close is not None:
            lines = lines[close + 1 :]
    body = "\n".join(lines).strip()
    if len(body.split("\n")) > 120:
        body = "\n".join(body.split("\n")[:120])
    return body


def main():
    """Generate skill + persona context for all agents."""
    agents = ["orchestrator", "researcher", "reviewer", "executor"]

    for agent in agents:
        # Generate skill context
        skill_context = generate_skill_context(agent)
        skill_file = ROOT / ".opencode" / "tools" / f"skill-context-{agent}.md"

        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(f"# Skills: {agent}\n\n{skill_context}")

        # Generate persona context
        persona_context = generate_persona_context(agent)
        persona_file = ROOT / ".opencode" / "tools" / f"persona-context-{agent}.md"

        with open(persona_file, "w", encoding="utf-8") as f:
            f.write(f"# Persona: {agent}\n\n{persona_context}")

        print(
            f"[AUTO-LOAD] {agent}: skill={len(skill_context)}c, persona={len(persona_context)}c"
        )


if __name__ == "__main__":
    main()
