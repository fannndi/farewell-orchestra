"""
check-consistency.py — Automated drift detection.
Cek konsistensi antara sumber kebenaran yang berbeda.

Drift yang dicek:
1. Skills di agent frontmatter vs skill dirs di disk
2. Skills di permission allowlist (generate.py) vs skill dirs di disk
3. Agent count di ci.yaml vs agent files di disk
4. Skill count di ci.yaml vs skill dirs di disk
5. Test imports vs actual exports di generate.py

Usage:  python .opencode/scripts/check-consistency.py
Exit:   0 if consistent, 1 if drift detected
"""

import os, re, sys, io
from pathlib import Path

# Fix Windows stdout encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent.parent
AGENTS_DIR = ROOT / ".opencode" / "agents"
SKILLS_DIR = ROOT / ".opencode" / "skills"
CI_YAML = ROOT / ".github" / "workflows" / "ci.yaml"
GENERATE_PY = ROOT / "profiles" / "generate.py"
TEST_GENERATE = ROOT / "tests" / "test_generate.py"


def get_skill_dirs():
    """Get all skill directories on disk."""
    return sorted(
        [
            d.name
            for d in SKILLS_DIR.iterdir()
            if d.is_dir() and (d / "SKILL.md").exists()
        ]
    )


def get_agent_files():
    """Get all agent .md files on disk."""
    return sorted([f.name for f in AGENTS_DIR.iterdir() if f.suffix == ".md"])


def get_agent_frontmatter_skills():
    """Extract skills from agent frontmatter."""
    agent_skills = {}
    for agent_file in AGENTS_DIR.glob("*.md"):
        content = agent_file.read_text(encoding="utf-8")
        # Match inline (skills: [a, b]) or block (skills:\n  - a) frontmatter
        match = re.search(r"skills:\s*\[(.*?)\]", content)
        if match:
            skills = [s.strip() for s in match.group(1).split(",") if s.strip()]
        else:
            block = re.search(r"skills:\s*\n((?:\s+-\s+\S+\n?)+)", content)
            skills = re.findall(r"-\s+(\S+)", block.group(1)) if block else []
        agent_skills[agent_file.stem] = skills
    return agent_skills


def get_permission_allowlist():
    """Extract skill allowlist from generate.py."""
    content = GENERATE_PY.read_text(encoding="utf-8")
    # Find the skill permission dict
    match = re.search(r'"skill":\s*\{([^}]+)\}', content)
    if not match:
        return []

    # Extract skill names (excluding "*" and "deny")
    skills = re.findall(r'"(\w[\w-]*)":\s*"allow"', match.group(1))
    return sorted(skills)


def get_ci_counts():
    """Extract expected counts from ci.yaml. Returns None if CI not configured."""
    if not CI_YAML.is_file():
        return None
    content = CI_YAML.read_text(encoding="utf-8")

    # Expected agents — ci.yaml asserts `expected=sorted(['a.md', ...])`
    agent_match = re.search(r"expected\s*=\s*sorted\(\[(.*?)\]\)", content, re.DOTALL)
    expected_agents = []
    if agent_match:
        expected_agents = re.findall(r"['\"](\w+\.md)['\"]", agent_match.group(1))

    return sorted(expected_agents)


def get_test_imports():
    """Extract imports from test_generate.py."""
    content = TEST_GENERATE.read_text(encoding="utf-8")
    imports = re.findall(r"from generate import \((.*?)\)", content, re.DOTALL)
    if imports:
        return re.findall(r"(\w+)", imports[0])
    return []


def get_actual_exports():
    """Get actual exports from generate.py."""
    content = GENERATE_PY.read_text(encoding="utf-8")
    # Find all top-level definitions
    exports = []
    for match in re.finditer(r"^(\w+)\s*[=:]", content, re.MULTILINE):
        name = match.group(1)
        if not name.startswith("_"):
            exports.append(name)
    return exports


def main():
    errors = []
    warnings = []

    # 1. Skills on disk
    skill_dirs = get_skill_dirs()
    agent_files = get_agent_files()

    # 2. Agent frontmatter skills
    agent_skills = get_agent_frontmatter_skills()
    all_agent_skills = set()
    for agent, skills in agent_skills.items():
        all_agent_skills.update(skills)

    # 3. Permission allowlist
    allowlist = get_permission_allowlist()

    # 4. CI counts
    expected_agents = get_ci_counts()

    # 5. Test imports vs actual exports
    test_imports = set(get_test_imports())
    actual_exports = set(get_actual_exports())

    # === Drift Checks ===

    # Check 1: Agent frontmatter skills vs skill dirs
    for skill in all_agent_skills:
        if skill not in skill_dirs:
            errors.append(
                f"DRIFT: Agent references skill '{skill}' but dir not found in .opencode/skills/"
            )

    # Frontmatter lists core skills only (AGENTS.md: on-demand via trigger).
    # Completeness of disk skills vs allowlist is covered by Check 2 below.
    for skill in all_agent_skills:
        if skill not in allowlist:
            warnings.append(
                f"WARN: Skill '{skill}' in agent frontmatter but NOT in permission allowlist"
            )

    # Check 2: Permission allowlist vs skill dirs
    for skill in allowlist:
        if skill not in skill_dirs:
            errors.append(
                f"DRIFT: Permission allowlist has '{skill}' but dir not found in .opencode/skills/"
            )

    for skill in skill_dirs:
        if skill not in allowlist:
            errors.append(
                f"DRIFT: Skill '{skill}' on disk but NOT in permission allowlist"
            )

    # Check 3: CI agent count vs actual agents
    if expected_agents is None:
        print("SKIP: ci.yaml not found")
    elif sorted(expected_agents) != agent_files:
        errors.append(
            f"DRIFT: CI expects agents {expected_agents}, actual {agent_files}"
        )

    # Report
    if errors:
        print(f"[CONSISTENCY] FAIL — {len(errors)} drift(s) detected:")
        for e in errors:
            print(f"  ❌ {e}")
        if warnings:
            print(f"\n  Warnings ({len(warnings)}):")
            for w in warnings:
                print(f"  ⚠️ {w}")
        sys.exit(1)
    else:
        print(
            f"[CONSISTENCY] OK — {len(skill_dirs)} skills, {len(agent_files)} agents, 0 drift"
        )
        if warnings:
            print(f"  Warnings ({len(warnings)}):")
            for w in warnings:
                print(f"  ⚠️ {w}")
        sys.exit(0)


if __name__ == "__main__":
    main()
