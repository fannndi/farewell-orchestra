"""
auto-load-skills.py — Auto-load critical skills AND persona at session start.
Dipanggil dari hook afterSessionStart atau afterGenerate.

Memuat skill + persona content ke memory sehingga agent tidak perlu manual load.
"""

import os, sys, json
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
    import re

    match = re.search(r"skills:\s*\n((?:\s+-\s+\S+\n?)+)", content)
    if match:
        return re.findall(r"-\s+(\S+)", match.group(1))
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


def generate_skill_context(agent_name):
    """Generate combined skill context for an agent."""
    skills = get_agent_skills(agent_name)
    context_parts = []

    for skill_name in skills:
        content = load_skill_content(skill_name)
        if content:
            # Extract key rules (first 50 lines or until ## section)
            lines = content.split("\n")
            key_lines = []
            for line in lines[:50]:
                key_lines.append(line)
                if line.startswith("## ") and len(key_lines) > 5:
                    break

            context_parts.append(
                f"=== SKILL: {skill_name} ===\n" + "\n".join(key_lines)
            )

    return "\n\n".join(context_parts)


def generate_persona_context(agent_name):
    """Generate persona context for an agent."""
    content = load_persona_content(agent_name)
    if not content:
        return ""

    # Extract key sections (first 100 lines)
    lines = content.split("\n")
    key_lines = []
    for line in lines[:100]:
        key_lines.append(line)

    return "\n".join(key_lines)


def main():
    """Generate skill + persona context for all agents."""
    agents = ["orchestrator", "researcher", "reviewer", "executor"]

    for agent in agents:
        # Generate skill context
        skill_context = generate_skill_context(agent)
        skill_file = ROOT / ".opencode" / "tools" / f"skill-context-{agent}.md"

        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(f"# Auto-loaded Skills for {agent}\n\n")
            f.write("This file is auto-generated. Do not edit manually.\n\n")
            f.write(skill_context)

        print(
            f"[AUTO-LOAD] Generated skill context for {agent}: {len(skill_context)} chars"
        )

        # Generate persona context
        persona_context = generate_persona_context(agent)
        persona_file = ROOT / ".opencode" / "tools" / f"persona-context-{agent}.md"

        with open(persona_file, "w", encoding="utf-8") as f:
            f.write(f"# Auto-loaded Persona for {agent}\n\n")
            f.write("This file is auto-generated. Do not edit manually.\n\n")
            f.write(persona_context)

        print(
            f"[AUTO-LOAD] Generated persona context for {agent}: {len(persona_context)} chars"
        )


if __name__ == "__main__":
    main()
