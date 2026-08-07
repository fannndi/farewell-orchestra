"""Unit tests for .opencode/tools/verify.py (structural adjacency checks)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".opencode" / "tools"))
from verify import check_stage_implement, check_stage_research, check_stage_review

VALID_REF = ".opencode/tools/verify.py:32"
FAR = "x" * 600


def _check(checks, name):
    for c in checks:
        if c["name"] == name:
            return c
    raise AssertionError(f"check not found: {name}")


def test_research_valid_refs_and_tags_adjacency_pass():
    claims = f"Finding: bug at {VALID_REF} — [P] [D2] confirmed"
    checks = check_stage_research(claims, [])
    assert _check(checks, "file:line references")["status"] == "PASS"
    assert _check(checks, "evidence tags [P/W/E/O] + depth [D1-D4]")["status"] == "PASS"
    assert _check(checks, "tag adjacency [P/W/E/O]+[D1-D4]")["status"] == "PASS"
    assert _check(checks, "evidence adjacency")["status"] == "PASS"


def test_research_without_tags_fails_and_warns_adjacency():
    claims = f"The bug is at {VALID_REF} and it breaks everything"
    checks = check_stage_research(claims, [])
    assert _check(checks, "evidence tags [P/W/E/O] + depth [D1-D4]")["status"] == "FAIL"
    assert _check(checks, "tag adjacency [P/W/E/O]+[D1-D4]")["status"] == "WARN"


def test_research_empty_claims_fails_non_empty():
    checks = check_stage_research("", [])
    assert _check(checks, "non-empty output")["status"] == "FAIL"


def test_research_missing_file_ref_fails():
    claims = "Issue at nonexistent_xyz.py:10 — [P]"
    checks = check_stage_research(claims, [])
    assert _check(checks, "file:line references")["status"] == "FAIL"


def test_research_uncertainty_marker_warns():
    claims = f"The bug is probably at {VALID_REF}"
    checks = check_stage_research(claims, [])
    assert _check(checks, "uncertainty markers")["status"] == "WARN"


def test_research_tag_far_from_ref_warns_adjacency():
    claims = f"Ref {VALID_REF}{FAR} [P] [D1]"
    checks = check_stage_research(claims, [])
    assert _check(checks, "tag adjacency [P/W/E/O]+[D1-D4]")["status"] == "WARN"


def test_review_priority_tags_and_blocking_ref_pass():
    checks = check_stage_review(
        "[BLOCKING] bug at .opencode/tools/verify.py:32 [D3]", []
    )
    assert _check(checks, "priority tags")["status"] == "PASS"
    assert _check(checks, "BLOCKING has file:line")["status"] == "PASS"


def test_review_blocking_requires_depth_d3():
    """BLOCKING finding without [D3]+ depth must FAIL the review depth gate."""
    checks = check_stage_review("[BLOCKING] src/auth.py:42 - JWT tanpa expiry [D1]", [])
    assert _check(checks, "depth [D1-D4]")["status"] == "FAIL"


def test_review_blocking_with_d3_passes():
    """BLOCKING finding with [D3] depth must PASS the review depth gate."""
    checks = check_stage_review("[BLOCKING] src/auth.py:42 - JWT tanpa expiry [D3]", [])
    assert _check(checks, "depth [D1-D4]")["status"] == "PASS"


def test_review_should_requires_depth_d2():
    """SHOULD finding with only [D1] must FAIL the review depth gate."""
    checks = check_stage_review("[SHOULD] src/auth.py:42 - N+1 query [D1]", [])
    assert _check(checks, "depth [D1-D4]")["status"] == "FAIL"


def test_implement_files_exist_pass():
    checks = check_stage_implement("done", ["tests/test_generate.py"])
    assert _check(checks, "files exist")["status"] == "PASS"
