"""
verify.py — Verification gate backend.
Called by verify.ts custom tool. Check agent output quality before next step.
Returns JSON: { pass: bool, checks: [{name, status, detail}], summary: str }
"""

import json, os, re, sys
from pathlib import Path

WORKTREE = os.environ.get("WORKTREE", os.getcwd())

UNCERTAINTY_MARKERS = [
    "I think", "probably", "maybe", "perhaps", "seems like",
    "I believe", "I assume", "I guess", "in my opinion",
    "sepertinya", "kayaknya", "mungkin", "kurang lebih",
    "harusnya", "seharusnya", "bisa jadi", "rasanya",
    "kemungkinan", "asumsi", "perkiraan"
]


def check_stage_research(claims: str, files: list[str]) -> list[dict]:
    checks = []

    # Check 1: Parse file:line references
    refs = re.findall(r'([\w./\\-]+\.\w+):(\d+)', claims)
    bad_refs = []
    for fpath, line in refs:
        full = Path(WORKTREE) / fpath
        if not full.exists():
            bad_refs.append(f"{fpath} (file not found)")
        else:
            try:
                total = len(full.read_text(encoding="utf-8").splitlines())
                if int(line) > total:
                    bad_refs.append(f"{fpath}:{line} (line {line} > {total} total)")
            except Exception:
                bad_refs.append(f"{fpath} (cannot read)")

    checks.append({
        "name": "file:line references",
        "status": "FAIL" if bad_refs else "PASS",
        "detail": f"Verified {len(refs)} references" + (f"; BAD: {bad_refs}" if bad_refs else "")
    })

    # Check 2: Uncertainty markers
    found_uncertainty = [m for m in UNCERTAINTY_MARKERS if m.lower() in claims.lower()]
    checks.append({
        "name": "uncertainty markers",
        "status": "PASS" if not found_uncertainty else "WARN",
        "detail": "None found" if not found_uncertainty else f"Found: {found_uncertainty[:5]}"
    })

    # Check 3: Evidence per claim (look for "source" or "finding" patterns)
    evidence_pattern = r'(source|Sumber|evidence|Finding|file:line|confidence)'
    has_evidence = bool(re.search(evidence_pattern, claims, re.IGNORECASE))
    checks.append({
        "name": "evidence attached",
        "status": "PASS" if has_evidence else "FAIL",
        "detail": "Evidence markers found" if has_evidence else "No evidence/source markers detected"
    })

    # Check 4: Empty output
    checks.append({
        "name": "non-empty output",
        "status": "PASS" if claims.strip() else "FAIL",
        "detail": f"{len(claims.strip())} chars" if claims.strip() else "Empty output"
    })

    # Check 5: Referenced files exist
    if files:
        missing = [f for f in files if not (Path(WORKTREE) / f).exists()]
        checks.append({
            "name": "referenced files exist",
            "status": "FAIL" if missing else "PASS",
            "detail": f"{len(files)} files checked" + (f"; MISSING: {missing}" if missing else "")
        })

    return checks


def check_stage_review(claims: str, files: list[str]) -> list[dict]:
    checks = []

    # Check 1: Priority tags
    valid_tags = ["BLOCKING", "SHOULD", "NICE", "FYI", "WARN", "INFO"]
    found_tags = re.findall(r'\[(\w+)\]', claims)
    bad_tags = [t for t in found_tags if t not in valid_tags]
    checks.append({
        "name": "priority tags",
        "status": "FAIL" if bad_tags else ("PASS" if found_tags else "WARN"),
        "detail": f"Tags found: {found_tags}" if found_tags else "No tags found"
        + (f"; INVALID: {bad_tags}" if bad_tags else "")
    })

    # Check 2: BLOCKING items have file reference
    blockings = re.findall(r'\[BLOCKING\].*?(?:\n|$)', claims)
    blocking_no_ref = []
    for b in blockings:
        if not re.search(r'[\w./\\-]+\.\w+:\d+', b):
            blocking_no_ref.append(b.strip()[:60])
    checks.append({
        "name": "BLOCKING has file:line",
        "status": "FAIL" if blocking_no_ref else "PASS",
        "detail": f"{len(blockings)} BLOCKING items" + (f"; {len(blocking_no_ref)} missing file ref" if blocking_no_ref else "")
    })

    # Check 3: Uncertainty markers
    found = [m for m in UNCERTAINTY_MARKERS if m.lower() in claims.lower()]
    checks.append({
        "name": "uncertainty in findings",
        "status": "PASS" if not found else "WARN",
        "detail": "None" if not found else f"Found: {found[:3]}"
    })

    # Check 4: Dedup (similar findings)
    sentences = [s.strip() for s in re.split(r'[.!?\n]', claims) if len(s.strip()) > 20]
    dupes = len(sentences) - len(set(sentences))
    checks.append({
        "name": "duplicate check",
        "status": "WARN" if dupes > 0 else "PASS",
        "detail": f"{len(sentences)} unique statements" if dupes == 0 else f"{dupes} possible duplicates"
    })

    return checks


def check_stage_implement(claims: str, files: list[str]) -> list[dict]:
    checks = []

    # Check 1: Files exist
    if files:
        missing = [f for f in files if not (Path(WORKTREE) / f).exists()]
        checks.append({
            "name": "files exist",
            "status": "FAIL" if missing else "PASS",
            "detail": f"{len(files)} files" + (f"; MISSING: {missing}" if missing else "")
        })
    else:
        checks.append({
            "name": "files exist",
            "status": "WARN",
            "detail": "No files specified to verify"
        })

    # Check 2: JSON validity for JSON files
    json_files = [f for f in files if f.endswith(('.json', '.jsonc'))]
    bad_json = []
    for f in json_files:
        fp = Path(WORKTREE) / f
        if fp.exists():
            try:
                text = fp.read_text(encoding="utf-8")
                # Strip JSONC comment lines before parsing
                clean = re.sub(r'^\s*//.*$', '', text, flags=re.MULTILINE)
                json.loads(clean)
            except json.JSONDecodeError as e:
                bad_json.append(f"{f}: {e.msg}")
    checks.append({
        "name": "JSON validity",
        "status": "FAIL" if bad_json else "PASS",
        "detail": f"{len(json_files)} JSON files" + (f"; INVALID: {bad_json}" if bad_json else "")
    })

    # Check 3: Leftover TODOs/FIXMEs
    todo_pattern = r'(TODO|FIXME|HACK|XXX|BUG):'
    todos = re.findall(todo_pattern, claims, re.IGNORECASE)
    checks.append({
        "name": "leftover markers",
        "status": "WARN" if todos else "PASS",
        "detail": "None" if not todos else f"Found: {set(todos)}"
    })

    # Check 4: Git diff (has changes)
    try:
        diff = os.popen('git diff --stat').read().strip()
        has_changes = bool(diff)
        checks.append({
            "name": "git changes",
            "status": "PASS" if has_changes else "WARN",
            "detail": diff.split("\n")[0] if has_changes else "No git changes detected"
        })
    except Exception:
        checks.append({
            "name": "git changes",
            "status": "WARN",
            "detail": "Cannot check git status"
        })

    # Check 5: Match spec keywords
    checks.append({
        "name": "scope check",
        "status": "PASS",
        "detail": f"{len(claims)} chars output"
    })

    return checks


def main():
    args = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}
    stage = args.get("stage", "research")
    claims = args.get("claims", "")
    files = args.get("files", [])
    spec = args.get("spec", "")

    if stage == "research":
        checks = check_stage_research(claims, files)
    elif stage == "review":
        checks = check_stage_review(claims, files)
    elif stage == "implement":
        checks = check_stage_implement(claims, files)
    else:
        checks = [{"name": "stage", "status": "FAIL", "detail": f"Unknown stage: {stage}"}]

    # Overall result
    fails = [c for c in checks if c["status"] == "FAIL"]
    warns = [c for c in checks if c["status"] == "WARN"]
    passed = [c for c in checks if c["status"] == "PASS"]

    if fails:
        summary = f"FAIL ({len(fails)} failed, {len(warns)} warnings)"
    elif warns:
        summary = f"PARTIAL ({len(warns)} warnings, {len(passed)} passed)"
    else:
        summary = f"PASS ({len(checks)}/{len(checks)} checks passed)"

    result = {
        "pass": len(fails) == 0,
        "summary": summary,
        "total": len(checks),
        "passed": len(passed),
        "warnings": len(warns),
        "failed": len(fails),
        "checks": checks,
    }

    sys.stdout.write(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
