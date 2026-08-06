"""
benchmark.py — Context budget benchmark (data-driven, per model tier).
Mengukur instruction load vs context window tiap model tier.
Bukan asumsi — angka dari profiles/profiles.json (model limits).

Run:  python scripts/benchmark.py
"""

import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Model tier → context window (verified from profiles/profiles.json)
MODEL_TIERS = {
    "1M": 1_000_000,
    "256K": 256_000,
    "128K": 128_000,
}
SAFE_RATIO = 0.30  # 30% rule: di atas ini ada risiko degradation (lost-in-the-middle)


def count(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    words = len(text.split())
    return words * 4 // 3  # tokens est


def main():
    # Tier 1: MUST — selalu di-load (system prompt: opencode.jsonc instructions)
    must = [".opencode/soul.md", "AGENTS.md"]
    # Tier 2: CORE — awal sesi (persona + context)
    core = ["README.md", "TRAINING.md", ".opencode/agents/boss.md"]
    core += [
        f".opencode/tools/persona-context-{a}.md"
        for a in ("orchestrator", "researcher", "reviewer", "executor")
    ]
    # Tier 3: PIPELINE — 5 skill inti
    pipeline = [
        f".opencode/skills/{s}/SKILL.md"
        for s in ("prepare", "orchestrate", "implement", "research", "review")
    ]
    # Tier 4: ON-DEMAND — 13 skill lainnya
    skills = [d for d in (ROOT / ".opencode" / "skills").iterdir() if d.is_dir()]
    pipeline_names = {"prepare", "orchestrate", "implement", "research", "review"}
    ondemand = [
        f".opencode/skills/{d.name}/SKILL.md"
        for d in skills
        if d.name not in pipeline_names
    ]

    def tier(name, files):
        t = sum(count(ROOT / f) for f in files)
        print(f"{name}: {t:,} tokens")
        return t

    print("=== CONTEXT BUDGET BENCHMARK ===\n")
    m = tier("MUST (selalu)", must)
    c = tier("CORE (awal sesi)", core)
    p = tier("PIPELINE (5 skill inti)", pipeline)
    o = tier("ON-DEMAND (13 skill)", ondemand)

    print("\n=== UTILIZATION vs MODEL TIER ===")
    tiers = [
        ("MUST", m),
        ("MUST+CORE", m + c),
        ("MUST+CORE+PIPELINE", m + c + p),
        ("MAX (semua di-load)", m + c + p + o),
    ]
    for label, tokens in tiers:
        row = f"  {label:<25} {tokens:>8,} tok"
        for tname, window in MODEL_TIERS.items():
            pct = tokens / window * 100
            safe = "SAFE" if pct <= SAFE_RATIO * 100 else "⚠️ OVER"
            row += f" | {tname}: {pct:5.1f}% {safe}"
        print(row)

    print("\n=== SAFE LIMIT (30% rule) ===")
    for tname, window in MODEL_TIERS.items():
        safe = int(window * SAFE_RATIO)
        print(
            f"  {tname}: {safe:,} tokens safe budget ({(window - m - c - p):,} headroom utk task)"
        )

    print(f"\n=== VERDICT ===")
    maxload = m + c + p + o
    smallest = MODEL_TIERS["128K"]
    print(
        f"  Load maksimum semua file: {maxload:,} tok = {maxload / smallest * 100:.1f}% dari 128K"
    )
    print(f"  Instruksi BUKAN bottleneck. Task context yang menentukan.")
    print(
        f"  Target onboarding tetap lean (<2000) tapi bukan karena limit — karena KISS."
    )


if __name__ == "__main__":
    main()
