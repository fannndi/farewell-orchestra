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


def extract_key_rules(content, max_lines=30):
    """Extract only key rules from content."""
    lines = content.split("\n")
    key_lines = []
    for line in lines[:max_lines]:
        # Skip empty lines and comments
        if line.strip() and not line.startswith("#"):
            key_lines.append(line)
    return "\n".join(key_lines)


def generate_skill_context(agent_name):
    """Generate compact skill context for an agent."""
    skills = get_agent_skills(agent_name)
    context_parts = []

    for skill_name in skills:
        content = load_skill_content(skill_name)
        if content:
            # Extract only key rules (first 20 lines)
            key_content = extract_key_rules(content, max_lines=20)
            context_parts.append(f"=== {skill_name} ===\n{key_content}")

    return "\n\n".join(context_parts)


def generate_persona_context(agent_name):
    """Generate compact persona context for an agent."""
    content = load_persona_content(agent_name)
    if not content:
        return ""
    # Extract only key sections (first 50 lines)
    return extract_key_rules(content, max_lines=50)


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
