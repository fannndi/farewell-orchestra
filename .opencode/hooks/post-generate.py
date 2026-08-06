"""
post-generate.py — Hook: validasi opencode.jsonc setelah generate.
Dipanggil otomatis dari hook runner OpenCode via hooks.jsonc.

Validasi:
1. Tool scoping (researcher/reviewer read-only, executor can edit)
2. Step budgets defined
3. Instructions tidak load semua agent file
4. Compaction rules defined kalau prune=true
"""

import json, os, sys


def load_config(config_path):
    """Load opencode.jsonc, strip comments."""
    with open(config_path, "r", encoding="utf-8") as f:
        raw = f.read()
    # Strip JSONC comments
    start = raw.index("{")
    return json.loads(raw[start:])


def validate(config_path):
    if not os.path.isfile(config_path):
        print("[HOOK] Config not found, skipping validation")
        return 0

    try:
        config = load_config(config_path)
    except Exception as e:
        print(f"[HOOK] Invalid JSON: {e}")
        return 1

    errors = []
    warnings = []

    # 1. Tool scoping
    agent_rules = {
        "researcher": {
            "forbidden": ["edit", "bash"],
            "required": ["webfetch", "websearch"],
        },
        "reviewer": {
            "forbidden": ["edit", "bash"],
            "required": ["webfetch", "websearch"],
        },
        "executor": {"required": ["edit"]},
    }

    for agent_name, rules in agent_rules.items():
        agent = config.get("agent", {}).get(agent_name)
        if not agent:
            warnings.append(f"{agent_name} agent not found")
            continue

        perms = agent.get("permission", {})

        for tool in rules.get("forbidden", []):
            val = perms.get(tool)
            if val == "allow":
                errors.append(
                    f"[SCOPE] {agent_name} should NOT have '{tool}' permission"
                )

        for tool in rules.get("required", []):
            val = perms.get(tool)
            if val != "allow":
                errors.append(f"[SCOPE] {agent_name} should have '{tool}' permission")

    # 2. Step budgets
    for name in ["orchestrator", "researcher", "reviewer", "executor"]:
        steps = config.get("agent", {}).get(name, {}).get("steps")
        if steps is None:
            warnings.append(f"[BUDGET] {name} steps not defined in config")

    # 3. Instructions
    instructions = " ".join(config.get("instructions", []))
    if "agents/*" in instructions:
        warnings.append(
            "[CONTEXT] instructions masih load semua agent file (*.md) - boros token"
        )

    # 4. Compaction
    prune = config.get("compaction", {}).get("prune", False)
    prune_rules = config.get("compaction", {}).get("prune_rules")
    if prune and not prune_rules:
        warnings.append(
            "[COMPACTION] prune=true but no prune_rules defined - random pruning risk"
        )

    # Report
    if errors:
        print("[HOOK] VALIDATION FAILED:")
        for e in errors:
            print(f"  {e}")
        return 1

    if warnings:
        print("[HOOK] Warnings:")
        for w in warnings:
            print(f"  {w}")

    agent_count = len(config.get("agent", {}))
    print(
        f"[HOOK] Config valid. {agent_count} agents, {len(errors)} errors, {len(warnings)} warnings"
    )
    return 0


if __name__ == "__main__":
    # Default config path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "..", "..", "opencode.jsonc")

    # Allow override via argument
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    sys.exit(validate(config_path))
