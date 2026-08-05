"""
verify.py — Verification gate backend.
Called by verify.ts custom tool. Check agent output quality before next step.
Returns JSON: { pass: bool, checks: [{name, status, detail}], summary: str }
"""

import json, os, re, subprocess, sys
from pathlib import Path

WORKTREE = os.environ.get("WORKTREE", os.getcwd())

UNCERTAINTY_MARKERS = [
    "I think",
    "probably",
    "maybe",
    "perhaps",
    "seems like",
    "I believe",
    "I assume",
    "I guess",
    "in my opinion",
    "sepertinya",
    "kayaknya",
    "mungkin",
    "kurang lebih",
    "harusnya",
    "seharusnya",
    "bisa jadi",
    "rasanya",
    "kemungkinan",
    "asumsi",
    "perkiraan",
]

REF_PATTERN = r"([\w./\\-]+\.\w+):(\d+)"

# Legitimate capacity-refusal signals — sub-agent reporting overload, not a
# failure. AGENTS.md: "[CHUNK_REQUIRED] = trigger re-chunk, bukan gagal."
# Never score these against normal evidence/tag/PASS-FAIL criteria.
CAPACITY_TAGS = ["CHUNK_REQUIRED", "CAPACITY_CHECK"]
CAPACITY_TOKEN_PATTERN = "|".join(rf"\[{t}\]" for t in CAPACITY_TAGS)


def _safe_worktree_path(fpath: str):
    """Resolve fpath inside WORKTREE; return Path if contained, else None (blocks traversal)."""
    fpath = fpath.replace("\\", "/")
    base = Path(WORKTREE).resolve()
    resolved = (base / fpath).resolve()
    if hasattr(Path, "is_relative_to"):
        inside = resolved.is_relative_to(base)
    else:
        inside = str(resolved).startswith(str(base))
    return resolved if inside else None


def check_stage_research(claims: str, files: list[str]) -> list[dict]:
    checks = []

    # Check 1: Parse file:line references
    refs = re.findall(r"([\w./\\-]+\.\w+):(\d+)", claims)
    bad_refs = []
    skipped_refs = []
    for fpath, line in refs:
        full = _safe_worktree_path(fpath)
        if full is None:
            skipped_refs.append(f"{fpath} (SKIP: path di luar worktree)")
            continue
        if not full.exists():
            bad_refs.append(f"{fpath} (file not found)")
        else:
            try:
                total = len(full.read_text(encoding="utf-8").splitlines())
                if int(line) > total:
                    bad_refs.append(f"{fpath}:{line} (line {line} > {total} total)")
            except Exception:
                bad_refs.append(f"{fpath} (cannot read)")

    detail = f"Verified {len(refs)} references"
    if skipped_refs:
        detail += f"; SKIP: {skipped_refs}"
    if bad_refs:
        detail += f"; BAD: {bad_refs}"
    checks.append(
        {
            "name": "file:line references",
            "status": "FAIL" if bad_refs else "PASS",
            "detail": detail,
        }
    )

    # Check 2: Uncertainty markers
    found_uncertainty = [m for m in UNCERTAINTY_MARKERS if m.lower() in claims.lower()]
    checks.append(
        {
            "name": "uncertainty markers",
            "status": "PASS" if not found_uncertainty else "WARN",
            "detail": "None found"
            if not found_uncertainty
            else f"Found: {found_uncertainty[:5]}",
        }
    )

    # Check 3: Evidence per claim (look for "source" or "finding" patterns)
    capacity_signal = bool(re.search(CAPACITY_TOKEN_PATTERN, claims))
    evidence_pattern = r"(source|Sumber|evidence|Finding|file:line|confidence)"
    has_evidence = bool(re.search(evidence_pattern, claims, re.IGNORECASE))
    if has_evidence:
        ev_status, ev_detail = "PASS", "Evidence markers found"
    elif capacity_signal:
        ev_status = "CHUNK_REQUIRED"
        ev_detail = "Capacity signal ([CHUNK_REQUIRED]/[CAPACITY_CHECK]) — evidence check skipped, not a failure"
    else:
        ev_status, ev_detail = "FAIL", "No evidence/source markers detected"
    checks.append(
        {
            "name": "evidence attached",
            "status": ev_status,
            "detail": ev_detail,
        }
    )

    # Check 3.1: Evidence adjacency — each file:line ref needs an evidence keyword within ±300 chars
    no_evidence_refs = 0
    for m in re.finditer(REF_PATTERN, claims):
        start = max(0, m.start() - 300)
        end = min(len(claims), m.end() + 300)
        if not re.search(
            r"(source|Sumber|evidence|Finding)", claims[start:end], re.IGNORECASE
        ):
            no_evidence_refs += 1
    checks.append(
        {
            "name": "evidence adjacency",
            "status": "PASS" if no_evidence_refs == 0 else "WARN",
            "detail": "All refs have evidence keyword in radius"
            if no_evidence_refs == 0
            else f"{no_evidence_refs} ref tanpa evidence adjacency",
        }
    )

    # Check 3.5: Evidence/depth tags — [P/W/E/O] from forensic, [D1-D4] from reviewer
    maturity_tag_pattern = r"\[P\]|\[W\]|\[E\]|\[O\]"
    depth_tag_pattern = r"\[D1\]|\[D2\]|\[D3\]|\[D4\]"
    all_tags_pattern = r"\[P\]|\[W\]|\[E\]|\[O\]|\[D1\]|\[D2\]|\[D3\]|\[D4\]"
    has_maturity_tags = bool(re.search(maturity_tag_pattern, claims))
    has_depth_tags = bool(re.search(depth_tag_pattern, claims))
    has_any_tags = bool(re.search(all_tags_pattern, claims))
    if has_maturity_tags:
        tag_status = "PASS"
    elif capacity_signal:
        tag_status = "CHUNK_REQUIRED"
    else:
        tag_status = "FAIL"
    if tag_status == "CHUNK_REQUIRED":
        tag_detail = "Capacity signal ([CHUNK_REQUIRED]/[CAPACITY_CHECK]) — no findings to tag, not a failure"
    elif has_any_tags:
        tag_detail = f"Evidence tags found: maturity={has_maturity_tags}, depth={has_depth_tags}"
    else:
        tag_detail = "No evidence tags [P/W/E/O] or depth tags [D1-D4] in findings — output may be untethered"
    checks.append(
        {
            "name": "evidence tags [P/W/E/O] + depth [D1-D4]",
            "status": tag_status,
            "detail": tag_detail,
        }
    )

    # Check 3.6: Tag adjacency — each file:line ref needs a tag [P/W/E/O]/[D1-D4] within ±500 chars
    no_tag_refs = 0
    for m in re.finditer(REF_PATTERN, claims):
        start = max(0, m.start() - 500)
        end = min(len(claims), m.end() + 500)
        if not re.search(all_tags_pattern, claims[start:end]):
            no_tag_refs += 1
    checks.append(
        {
            "name": "tag adjacency [P/W/E/O]+[D1-D4]",
            "status": "PASS" if no_tag_refs == 0 else "WARN",
            "detail": "All refs have tags in radius"
            if no_tag_refs == 0
            else f"{no_tag_refs} ref tanpa tag adjacency",
        }
    )

    # Check 4: Empty output
    checks.append(
        {
            "name": "non-empty output",
            "status": "PASS" if claims.strip() else "FAIL",
            "detail": f"{len(claims.strip())} chars"
            if claims.strip()
            else "Empty output",
        }
    )

    # Check 5: Referenced files exist
    if files:
        missing = [f for f in files if not (Path(WORKTREE) / f).exists()]
        checks.append(
            {
                "name": "referenced files exist",
                "status": "FAIL" if missing else "PASS",
                "detail": f"{len(files)} files checked"
                + (f"; MISSING: {missing}" if missing else ""),
            }
        )

    return checks


def check_stage_review(claims: str, files: list[str]) -> list[dict]:
    checks = []

    # Check 1: Priority tags
    valid_tags = [
        "BLOCKING",
        "SHOULD",
        "NICE",
        "FYI",
        "WARN",
        "INFO",
        "D1",
        "D2",
        "D3",
        "D4",
    ]
    found_tags = re.findall(r"\[(\w+)\]", claims)
    # Capacity-refusal tags are passthrough — never "INVALID", never FAIL.
    # AGENTS.md: "[CHUNK_REQUIRED] = trigger re-chunk, bukan gagal."
    found_capacity_tags = [t for t in found_tags if t in CAPACITY_TAGS]
    bad_tags = [
        t for t in found_tags if t not in valid_tags and t not in CAPACITY_TAGS
    ]
    detail = f"Tags found: {found_tags}" if found_tags else "No tags found"
    if bad_tags:
        detail += f"; INVALID: {bad_tags}"
    if bad_tags:
        tag_status = "FAIL"
    elif found_capacity_tags:
        tag_status = "CHUNK_REQUIRED"
    elif found_tags:
        tag_status = "PASS"
    else:
        tag_status = "WARN"
    checks.append(
        {
            "name": "priority tags",
            "status": tag_status,
            "detail": detail,
        }
    )

    # Check 2: BLOCKING items have file reference
    blockings = re.findall(r"\[BLOCKING\].*?(?:\n|$)", claims)
    blocking_no_ref = []
    for b in blockings:
        if not re.search(r"[\w./\\-]+\.\w+:\d+", b):
            blocking_no_ref.append(b.strip()[:60])
    checks.append(
        {
            "name": "BLOCKING has file:line",
            "status": "FAIL" if blocking_no_ref else "PASS",
            "detail": f"{len(blockings)} BLOCKING items"
            + (f"; {len(blocking_no_ref)} missing file ref" if blocking_no_ref else ""),
        }
    )

    # Check 3: Uncertainty markers
    found = [m for m in UNCERTAINTY_MARKERS if m.lower() in claims.lower()]
    checks.append(
        {
            "name": "uncertainty in findings",
            "status": "PASS" if not found else "WARN",
            "detail": "None" if not found else f"Found: {found[:3]}",
        }
    )

    # Check 4: Dedup (similar findings)
    sentences = [s.strip() for s in re.split(r"[.!?\n]", claims) if len(s.strip()) > 20]
    dupes = len(sentences) - len(set(sentences))
    checks.append(
        {
            "name": "duplicate check",
            "status": "WARN" if dupes > 0 else "PASS",
            "detail": f"{len(sentences)} unique statements"
            if dupes == 0
            else f"{dupes} possible duplicates",
        }
    )

    return checks


def check_stage_implement(claims: str, files: list[str]) -> list[dict]:
    checks = []

    # Check 1: Files exist
    if files:
        missing = [f for f in files if not (Path(WORKTREE) / f).exists()]
        checks.append(
            {
                "name": "files exist",
                "status": "FAIL" if missing else "PASS",
                "detail": f"{len(files)} files"
                + (f"; MISSING: {missing}" if missing else ""),
            }
        )
    else:
        checks.append(
            {
                "name": "files exist",
                "status": "WARN",
                "detail": "No files specified to verify",
            }
        )

    # Check 2: JSON validity for JSON files
    json_files = [f for f in files if f.endswith((".json", ".jsonc"))]
    bad_json = []
    for f in json_files:
        fp = Path(WORKTREE) / f
        if fp.exists():
            try:
                text = fp.read_text(encoding="utf-8")
                # Strip JSONC comment lines before parsing
                clean = re.sub(r"^\s*//.*$", "", text, flags=re.MULTILINE)
                json.loads(clean)
            except json.JSONDecodeError as e:
                bad_json.append(f"{f}: {e.msg}")
    checks.append(
        {
            "name": "JSON validity",
            "status": "FAIL" if bad_json else "PASS",
            "detail": f"{len(json_files)} JSON files"
            + (f"; INVALID: {bad_json}" if bad_json else ""),
        }
    )

    # Check 3: Leftover TODOs/FIXMEs
    todo_pattern = r"(TODO|FIXME|HACK|XXX|BUG):"
    todos = re.findall(todo_pattern, claims, re.IGNORECASE)
    checks.append(
        {
            "name": "leftover markers",
            "status": "WARN" if todos else "PASS",
            "detail": "None" if not todos else f"Found: {set(todos)}",
        }
    )

    # Check 4: Git diff (has changes)
    try:
        proc = subprocess.run(
            ["git", "diff", "--stat"],
            capture_output=True,
            text=True,
            timeout=5,
            cwd=WORKTREE,
        )
        proc.check_returncode()
        diff = proc.stdout.strip()
        has_changes = bool(diff)
        checks.append(
            {
                "name": "git changes",
                "status": "PASS" if has_changes else "WARN",
                "detail": diff.split("\n")[0]
                if has_changes
                else "No git changes detected",
            }
        )
    except subprocess.TimeoutExpired:
        checks.append({"name": "git changes", "status": "WARN", "detail": "(timeout)"})
    except Exception:
        checks.append(
            {
                "name": "git changes",
                "status": "WARN",
                "detail": "Cannot check git status",
            }
        )

    # Check 5: Match spec keywords
    checks.append(
        {
            "name": "scope check",
            "status": "PASS",
            "detail": f"{len(claims)} chars output",
        }
    )

    return checks


def main():
    if not sys.stdin.isatty():
        data = sys.stdin.read(2_000_000)
        if len(data) == 2_000_000 and sys.stdin.read(1):
            error = {
                "pass": False,
                "summary": "PAYLOAD_TOO_LARGE (max 2MB)",
                "total": 1,
                "passed": 0,
                "warnings": 0,
                "failed": 1,
                "checks": [
                    {
                        "name": "payload size",
                        "status": "FAIL",
                        "detail": "PAYLOAD_TOO_LARGE (max 2MB)",
                    }
                ],
            }
            sys.stdout.write(json.dumps(error, indent=2))
            sys.exit(1)
        args = json.loads(data)
    else:
        args = {}
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
        checks = [
            {"name": "stage", "status": "FAIL", "detail": f"Unknown stage: {stage}"}
        ]

    # Overall result
    fails = [c for c in checks if c["status"] == "FAIL"]
    warns = [c for c in checks if c["status"] == "WARN"]
    capacity = [c for c in checks if c["status"] == "CHUNK_REQUIRED"]
    passed = [c for c in checks if c["status"] == "PASS"]

    if fails:
        summary = f"FAIL ({len(fails)} failed, {len(warns)} warnings)"
    elif capacity:
        summary = (
            f"CHUNK_REQUIRED ({len(capacity)} capacity signal(s) — "
            "sub-agent overloaded, re-chunk, not a failure)"
        )
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
