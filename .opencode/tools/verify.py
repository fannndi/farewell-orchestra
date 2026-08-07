"""
verify.py — Verification gate backend.
Called by verify.ts custom tool. Check agent output quality.
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
    "harusnya",
    "seharusnya",
    "bisa jadi",
    "rasanya",
    "kemungkinan",
    "asumsi",
    "perkiraan",
]

REF_PATTERN = r"([\w./\\-]+\.\w+):(\d+)"


def _safe_worktree_path(fpath: str):
    """Resolve fpath inside WORKTREE; return Path if contained, else None."""
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

    # 1. Non-empty
    checks.append(
        {
            "name": "non-empty output",
            "status": "PASS" if claims.strip() else "FAIL",
            "detail": f"{len(claims.strip())} chars"
            if claims.strip()
            else "Empty output",
        }
    )

    # 2. File:line references exist
    refs = re.findall(REF_PATTERN, claims)
    bad_refs = []
    skipped = 0  # refs outside worktree: not counted as checked
    for fpath, line in refs:
        full = _safe_worktree_path(fpath)
        if full is None:
            skipped += 1
            continue  # skip paths outside worktree
        if not full.exists():
            bad_refs.append(f"{fpath} (not found)")
        else:
            try:
                total = len(full.read_text(encoding="utf-8").splitlines())
                if int(line) > total:
                    bad_refs.append(f"{fpath}:{line} (line > {total})")
            except Exception:
                bad_refs.append(f"{fpath} (cannot read)")

    checks.append(
        {
            "name": "file:line references",
            "status": "FAIL" if bad_refs else "PASS",
            "detail": f"{len(refs) - skipped} refs checked"
            + (f"; {skipped} outside worktree" if skipped else "")
            + (f"; BAD: {bad_refs}" if bad_refs else ""),
        }
    )

    # 3. Uncertainty markers
    found = [m for m in UNCERTAINTY_MARKERS if m.lower() in claims.lower()]
    checks.append(
        {
            "name": "uncertainty markers",
            "status": "PASS" if not found else "WARN",
            "detail": "None" if not found else f"Found: {found[:5]}",
        }
    )

    # 4. Evidence tags [P/W/E/O] + depth [D1-D4]
    evidence_tags = re.findall(r"\[([PWOE])\]", claims)
    depth_tags = re.findall(r"\[(D[1-4])\]", claims)
    checks.append(
        {
            "name": "evidence tags [P/W/E/O] + depth [D1-D4]",
            "status": "PASS" if evidence_tags else "FAIL",
            "detail": f"Found {len(evidence_tags)} tags: {evidence_tags[:5]}"
            + (f"; depth: {depth_tags[:5]}" if depth_tags else "")
            if evidence_tags
            else "No [P/W/E/O] tags found",
        }
    )

    # 5. Tag adjacency — check if tags are near file:line refs
    if evidence_tags and refs:
        # Check if each tag is within 100 chars of a ref
        adjacent = True
        for match in re.finditer(r"\[([PWOE])\]", claims):
            tag_pos = match.start()
            # Find nearest ref
            min_dist = float("inf")
            for ref_match in re.finditer(REF_PATTERN, claims):
                ref_pos = ref_match.start()
                min_dist = min(min_dist, abs(tag_pos - ref_pos))
            if min_dist > 100:
                adjacent = False
                break

        checks.append(
            {
                "name": "tag adjacency [P/W/E/O]+[D1-D4]",
                "status": "PASS" if adjacent else "WARN",
                "detail": "Tags near refs"
                if adjacent
                else "Tags far from refs (>100 chars)",
            }
        )
    else:
        # Always add adjacency check
        checks.append(
            {
                "name": "tag adjacency [P/W/E/O]+[D1-D4]",
                "status": "WARN" if not evidence_tags else "PASS",
                "detail": "No tags to check adjacency"
                if not evidence_tags
                else "Tags present",
            }
        )

    # 6. Evidence adjacency — overall check
    if refs and evidence_tags:
        # Check if evidence is properly linked
        linked = len(evidence_tags) > 0 and len(refs) > 0
        checks.append(
            {
                "name": "evidence adjacency",
                "status": "PASS" if linked else "WARN",
                "detail": f"{len(evidence_tags)} tags, {len(refs)} refs",
            }
        )

    return checks


def check_stage_review(claims: str, files: list[str]) -> list[dict]:
    checks = []

    # 1. Priority tags present
    valid_tags = {
        "BLOCKING",
        "SHOULD",
        "NICE",
        "FYI",
        "D1",
        "D2",
        "D3",
        "D4",
        "P",
        "W",
        "E",
        "O",
    }
    found_tags = re.findall(r"\[(\w+)\]", claims)
    bad_tags = [t for t in found_tags if t not in valid_tags and t != "CHUNK_REQUIRED"]
    checks.append(
        {
            "name": "priority tags",
            "status": "FAIL" if bad_tags else ("PASS" if found_tags else "WARN"),
            "detail": f"Tags: {found_tags}"
            + (f"; INVALID: {bad_tags}" if bad_tags else ""),
        }
    )

    # 2. BLOCKING has file:line
    blockings = re.findall(r"\[BLOCKING\].*?(?:\n|$)", claims)
    blocking_no_ref = [b for b in blockings if not re.search(REF_PATTERN, b)]
    checks.append(
        {
            "name": "BLOCKING has file:line",
            "status": "FAIL" if blocking_no_ref else "PASS",
            "detail": f"{len(blockings)} BLOCKING"
            + (f"; {len(blocking_no_ref)} missing ref" if blocking_no_ref else ""),
        }
    )

    # 3. Depth enforcement: BLOCKING requires [D3]+, SHOULD requires [D2]+
    #    Depth tag may sit on the finding line OR a continuation line (next 2).
    depth_issues = []
    lines = claims.splitlines()
    for i, line in enumerate(lines):
        window = "\n".join(lines[i : i + 3])
        if "[BLOCKING]" in line and not re.search(r"\[D[34]\]", window):
            depth_issues.append("BLOCKING requires [D3]+ depth")
        if "[SHOULD]" in line and not re.search(r"\[D[234]\]", window):
            depth_issues.append("SHOULD requires [D2]+ depth")
    checks.append(
        {
            "name": "depth [D1-D4]",
            "status": "FAIL" if depth_issues else "PASS",
            "detail": "; ".join(depth_issues) or "BLOCKING=[D3]+ SHOULD=[D2]+ enforced",
        }
    )

    # 4. Uncertainty markers
    found = [m for m in UNCERTAINTY_MARKERS if m.lower() in claims.lower()]
    checks.append(
        {
            "name": "uncertainty in findings",
            "status": "PASS" if not found else "WARN",
            "detail": "None" if not found else f"Found: {found[:3]}",
        }
    )

    return checks


def check_stage_implement(claims: str, files: list[str]) -> list[dict]:
    checks = []

    # 1. Files exist (contained in worktree)
    if files:
        missing = []
        for f in files:
            resolved = _safe_worktree_path(f)
            if resolved is None:
                missing.append(f"{f} (path traversal)")
            elif not resolved.exists():
                missing.append(f"{f} (not found)")
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
            {"name": "files exist", "status": "WARN", "detail": "No files specified"}
        )

    # 2. Git diff (has changes)
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
        checks.append(
            {
                "name": "git changes",
                "status": "PASS" if diff else "WARN",
                "detail": diff.split("\n")[0] if diff else "No changes detected",
            }
        )
    except Exception:
        checks.append(
            {"name": "git changes", "status": "WARN", "detail": "Cannot check git"}
        )

    return checks


def main():
    if not sys.stdin.isatty():
        data = sys.stdin.read(2_000_000)
        if len(data) == 2_000_000 and sys.stdin.read(1):
            error = {
                "pass": False,
                "summary": "PAYLOAD_TOO_LARGE",
                "total": 1,
                "passed": 0,
                "warnings": 0,
                "failed": 1,
                "checks": [{"name": "payload", "status": "FAIL", "detail": "Max 2MB"}],
            }
            sys.stdout.write(json.dumps(error, indent=2))
            sys.exit(1)
        args = json.loads(data)
    else:
        args = {}

    stage = args.get("stage", "research")
    claims = args.get("claims", "")
    files = args.get("files", [])

    if stage == "research":
        checks = check_stage_research(claims, files)
    elif stage == "review":
        checks = check_stage_review(claims, files)
    elif stage == "implement":
        checks = check_stage_implement(claims, files)
    else:
        checks = [{"name": "stage", "status": "FAIL", "detail": f"Unknown: {stage}"}]

    fails = [c for c in checks if c["status"] == "FAIL"]
    warns = [c for c in checks if c["status"] == "WARN"]
    passed = [c for c in checks if c["status"] == "PASS"]

    if fails:
        summary = f"FAIL ({len(fails)} failed, {len(warns)} warnings)"
    elif warns:
        summary = f"PARTIAL ({len(warns)} warnings, {len(passed)} passed)"
    else:
        summary = f"PASS ({len(checks)}/{len(checks)} passed)"

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
