"""
check-all.py — Full health check, satu command.
Menjalankan SEMUA verifikasi project. Output: PASS/FAIL per check + ringkasan.

Run:  python scripts/check-all.py
Exit: 0 = all green, 1 = ada yang fail
"""

import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Derive test-file count so the label never goes stale
TEST_FILES = sorted((ROOT / "tests").glob("test_*.py"))

# Windows console default cp1252 — paksa UTF-8 biar output Unicode aman
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CHECKS = [
    (
        "pytest ({} test files)".format(len(TEST_FILES)),
        ["python", "-m", "pytest", "tests/", "-q"],
    ),
    ("effectiveness (persona/skill)", ["python", "tests/test_effectiveness.py"]),
    ("consistency (drift)", ["python", ".opencode/scripts/check-consistency.py"]),
    ("links (broken refs)", ["python", ".opencode/scripts/check-links.py"]),
    ("stress-test (config)", ["python", "scripts/stress-test.py"]),
    ("profiles validate", ["python", "profiles/generate.py", "--validate"]),
    ("benchmark (context budget)", ["python", "scripts/benchmark.py"]),
]

# Recovery hints per check key — printed after a FAIL line
HINTS = {
    "pytest": "Fix: python -m pytest tests/ -q --tb=short",
    "effectiveness": "Fix: python tests/test_effectiveness.py",
    "consistency": "Fix: python .opencode/scripts/check-consistency.py",
    "links": "Fix: python .opencode/scripts/check-links.py",
    "stress-test": "Fix: python scripts/stress-test.py",
    "profiles": "Fix: python profiles/generate.py --validate",
    "benchmark": "Fix: python scripts/benchmark.py",
}


def main():
    print("=== CHECK-ALL: Full Health ===\n")
    failed = []
    for name, cmd in CHECKS:
        try:
            r = subprocess.run(
                cmd,
                cwd=ROOT,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            tail = (r.stdout or r.stderr).strip().splitlines()
            tail = tail[-1] if tail else ""
            ok = r.returncode == 0
        except Exception as e:
            ok, tail = False, str(e)
        mark = "PASS" if ok else "FAIL"
        print(f"  [{mark}] {name}: {tail}")
        if not ok:
            failed.append(name)
            hint = HINTS.get(name.split(" ")[0].split("(")[0])
            if hint:
                print(f"         {hint}")

    print(
        f"\n=== RESULT: {len(CHECKS) - len(failed)}/{len(CHECKS)} PASS"
        + (f" — FAIL: {failed}" if failed else " — ALL GREEN ===")
    )
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
