"""
test_effectiveness.py — Test effectiveness of persona + skill system.
Measures actual behavior, not claims.

Usage:  python tests/test_effectiveness.py
"""

import json, os, sys, time, io
from pathlib import Path

# Fix Windows stdout encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = ROOT / ".opencode" / "agents"
SKILLS_DIR = ROOT / ".opencode" / "skills"


def test_persona_completeness():
    """Check if personas have required sections."""
    results = []
    required_sections = [
        "Identity",
        "WAJIB LOAD",
        "Skill Triggers",
        "Proactive Behavior",
        "Decision Tree",
        "Output",
    ]

    for agent_file in AGENTS_DIR.glob("*.md"):
        if agent_file.name == "boss.md" or agent_file.name == "soul.md":
            continue

        content = agent_file.read_text(encoding="utf-8")
        missing = []

        for section in required_sections:
            if section not in content:
                missing.append(section)

        results.append(
            {
                "agent": agent_file.stem,
                "complete": len(missing) == 0,
                "missing": missing,
                "sections_found": len(required_sections) - len(missing),
            }
        )

    return results


def test_skill_activation():
    """Check if skills have activation conditions."""
    results = []

    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        content = skill_file.read_text(encoding="utf-8")

        has_activation = "activation:" in content
        has_trigger = "trigger:" in content

        results.append(
            {
                "skill": skill_dir.name,
                "has_activation": has_activation,
                "has_trigger": has_trigger,
                "complete": has_activation or has_trigger,
            }
        )

    return results


def test_skill_overlap():
    """Check for skill overlap between agents."""
    agent_skills = {}

    for agent_file in AGENTS_DIR.glob("*.md"):
        if agent_file.name in ("boss.md", "soul.md"):
            continue

        content = agent_file.read_text(encoding="utf-8")

        # Extract skills from frontmatter
        import re

        match = re.search(r"skills:\s*\[(.*?)\]", content)
        if match:
            skills = [s.strip() for s in match.group(1).split(",")]
            agent_skills[agent_file.stem] = skills

    # Check for overlap
    overlaps = []
    agents = list(agent_skills.keys())
    for i in range(len(agents)):
        for j in range(i + 1, len(agents)):
            common = set(agent_skills[agents[i]]) & set(agent_skills[agents[j]])
            if common:
                overlaps.append(
                    {"agents": [agents[i], agents[j]], "common_skills": list(common)}
                )

    return overlaps


def test_conciseness():
    """Check if persona files are concise."""
    results = []

    for agent_file in AGENTS_DIR.glob("*.md"):
        if agent_file.name in ("boss.md", "soul.md"):
            continue

        content = agent_file.read_text(encoding="utf-8")
        lines = len(content.split("\n"))
        words = len(content.split())

        results.append(
            {
                "agent": agent_file.stem,
                "lines": lines,
                "words": words,
                "concise": lines < 80,
            }
        )

    return results


def main():
    print("=== EFFECTIVENESS TEST ===\n")

    # Test 1: Persona completeness
    print("1. PERSONA COMPLETENESS")
    persona_results = test_persona_completeness()
    for r in persona_results:
        status = "✅" if r["complete"] else "❌"
        print(f"   {status} {r['agent']}: {r['sections_found']}/6 sections")
        if r["missing"]:
            print(f"      Missing: {', '.join(r['missing'])}")

    # Test 2: Skill activation
    print("\n2. SKILL ACTIVATION CONDITIONS")
    skill_results = test_skill_activation()
    with_activation = sum(1 for r in skill_results if r["has_activation"])
    with_trigger = sum(1 for r in skill_results if r["has_trigger"])
    print(f"   With activation: {with_activation}/{len(skill_results)}")
    print(f"   With trigger: {with_trigger}/{len(skill_results)}")

    # Test 3: Skill overlap
    print("\n3. SKILL OVERLAP")
    overlaps = test_skill_overlap()
    if overlaps:
        for o in overlaps:
            print(
                f"   ⚠️ {o['agents'][0]} + {o['agents'][1]}: {', '.join(o['common_skills'])}"
            )
    else:
        print("   ✅ No overlap")

    # Test 4: Conciseness
    print("\n4. CONCISENESS")
    concise_results = test_conciseness()
    for r in concise_results:
        status = "✅" if r["concise"] else "❌"
        print(f"   {status} {r['agent']}: {r['lines']} lines, {r['words']} words")

    # Summary
    print("\n=== SUMMARY ===")
    persona_pass = sum(1 for r in persona_results if r["complete"])
    skill_pass = sum(1 for r in skill_results if r["complete"])
    concise_pass = sum(1 for r in concise_results if r["concise"])

    print(f"Personas: {persona_pass}/4 complete")
    print(f"Skills: {skill_pass}/{len(skill_results)} with activation")
    print(f"Conciseness: {concise_pass}/4 concise")
    print(f"Overlap: {len(overlaps)} conflicts")


if __name__ == "__main__":
    main()
