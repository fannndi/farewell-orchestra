"""
auto-load-skills.py — Auto-load critical skills at session start.
Dipanggil dari hook afterSessionStart atau afterGenerate.

Memuat skill content ke memory sehingga agent tidak perlu manual load.
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


def main():
    """Generate skill context for all agents."""
    agents = ["orchestrator", "researcher", "reviewer", "executor"]

    for agent in agents:
        context = generate_skill_context(agent)
        output_file = ROOT / ".opencode" / "tools" / f"skill-context-{agent}.md"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# Auto-loaded Skills for {agent}\n\n")
            f.write("This file is auto-generated. Do not edit manually.\n\n")
            f.write(context)

        print(f"[AUTO-LOAD] Generated skill context for {agent}: {len(context)} chars")


if __name__ == "__main__":
    main()
