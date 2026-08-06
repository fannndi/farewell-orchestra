"""
stress-test.py — Multi-model config validation for Farewell Orchestra.
Verifies every profile/agent has valid model refs, all skills allowlisted,
permission scoping correct. Structural readiness check (runtime dispatch is separate).

Run:  python scripts/stress-test.py
"""

import io, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "profiles"))
from generate import (
    load_profiles,
    validate_registry,
    build_provider_models,
    AGENT_TEMPLATES,
)

FAIL = 0


def check(name, ok, detail=""):
    global FAIL
    status = "PASS" if ok else "FAIL"
    if not ok:
        FAIL += 1
    print(f"  [{status}] {name}{' — ' + detail if detail else ''}")


def main():
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace"
        )

    print("=== STRESS TEST: Multi-Model Config ===\n")

    # 1. Registry valid
    print("1. PROFILE REGISTRY")
    reg = load_profiles()
    errors = [e for e in validate_registry(reg) if not e.startswith("[WARN]")]
    check("registry valid", len(errors) == 0, "; ".join(errors[:3]))

    # 2. Every profile: all 4 agents have models referencing registry
    print("\n2. PROFILE → AGENT MODEL REFS")
    for p in reg["profiles"]:
        name = p["name"]
        models = build_provider_models(reg, p)
        ok = True
        for role in ("orchestrator", "researcher", "reviewer", "executor"):
            ad = p["agents"][role]
            m = ad["model"] if isinstance(ad, dict) else ad
            short = m.replace("9router/", "") if m.startswith("9router/") else m
            if short not in models:
                ok = False
                print(f"    ⚠ {name}/{role}: model '{m}' not in provider models")
        check(f"profile '{name}' models valid", ok)

    # 3. Skill allowlist = skills on disk (read from active opencode.jsonc,
    #    since AGENT_TEMPLATES[*].permission.skill is a plain "allow" string)
    print("\n3. SKILL ALLOWLIST COMPLETE")
    skill_dirs = {
        d.name
        for d in (ROOT / ".opencode" / "skills").iterdir()
        if d.is_dir() and (d / "SKILL.md").exists()
    }
    oc = ROOT / "opencode.jsonc"
    if not oc.exists():
        check("opencode.jsonc exists", False)
    else:
        raw = oc.read_text(encoding="utf-8")
        allow = json.loads(raw[raw.index("{") :])["permission"]["skill"]
        allowlisted = {k for k, v in allow.items() if k != "*" and v == "allow"}
        missing = sorted(skill_dirs - allowlisted)
        phantom = sorted(allowlisted - skill_dirs)
        check("all disk skills allowlisted", len(missing) == 0, f"missing: {missing}")
        check("no phantom skills", len(phantom) == 0, f"phantom: {phantom}")

    # 4. Permission scoping
    print("\n4. PERMISSION SCOPING")
    for role in ("researcher", "reviewer"):
        perm = AGENT_TEMPLATES[role]["permission"]
        check(f"{role} edit deny", perm["edit"] == "deny")
        check(f"{role} bash deny", perm["bash"] == "deny")
        read = perm.get("read", {})
        check(
            f"{role} .env deny",
            isinstance(read, dict) and any(".env" in k for k in read),
            str(read)[:80],
        )
    ex = AGENT_TEMPLATES["executor"]["permission"]
    check(
        "executor granular bash",
        isinstance(ex["bash"], dict) and ex["bash"].get("*") == "ask",
    )

    # 5. OpenCode config sync
    print("\n5. OPENCODE CONFIG SYNC")
    check("opencode.jsonc exists", oc.exists())
    if oc.exists():
        raw = oc.read_text(encoding="utf-8")
        has_docs = "C:/Users/FANNNDI/Documents/**" in raw
        has_env_deny = ".env" in raw and "deny" in raw
        check("external_directory Documents/**", has_docs)
        check(".env deny present", has_env_deny)

    print(f"\n=== RESULT: {FAIL} FAIL, {'ALL PASS' if FAIL == 0 else 'FIX NEEDED'} ===")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
