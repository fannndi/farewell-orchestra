"""
benchmark-degradation.py — Readiness check + runbook untuk empirical degradation test.
BUKAN pengukuran nyata — verifikasi struktur harness siap. Jalankan manual per sesi
untuk data empiris (butuh model access). Lihat TRAINING.md Mode B untuk prosedur.

Run:  python scripts/benchmark-degradation.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Windows console default cp1252 — paksa UTF-8 biar karakter Unicode aman
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def check(name, ok, detail=""):
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {name}{' — ' + detail if detail else ''}")
    return ok


def main():
    print("=== DEGRADATION HARNESS ===\n")

    print("1. HARNESS STRUCTURE")
    ok = True
    ok &= check("benchmark.py exists", (ROOT / "scripts/benchmark.py").exists())
    ok &= check("stress-test.py exists", (ROOT / "scripts/stress-test.py").exists())
    ok &= check("test_pipeline.py exists", (ROOT / "tests/test_pipeline.py").exists())

    print("\n2. DEGRADATION TEST DESIGN (rubric)")
    print("  Task standar: 'Review src untuk security + KISS' (5 planted issues)")
    print("  Levels: 10% / 30% / 50% / 70% / 90% context fill")
    print(
        "  Rubric (0-3): completeness, KISS adherence, evidence quality, false positives"
    )
    print("  Runs: 5 per level (25 total) — paired t-test α=0.05")

    print("\n3. RUNBOOK (manual, butuh model access)")
    print("  Langkah: (1) switch profile, (2) dispatch sub-agent dengan")
    print("  prompt + filler sampai level target, (3) nilai output via rubric,")
    print("  (4) catat hasil di Farewell-Knowlage/Session.md")
    print("  Stopping rule: sharp quality drop antara 70-90% → catat threshold model")

    print("\n4. READINESS")
    ok &= check(
        "128K floor principle documented",
        "128K" in (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
    )
    ok &= check(
        "step-based estimation exists",
        "Step-Based"
        in (ROOT / ".opencode/skills/context-window/SKILL.md").read_text(
            encoding="utf-8"
        ),
    )

    print(f"\n=== RESULT: {'ALL PASS — harness ready' if ok else 'FIX NEEDED'} ===")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
