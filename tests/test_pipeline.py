"""
test_pipeline.py — End-to-end pipeline structural tests.
Validates the full Request → prepare → research/review → orchestrate → implement → report flow
by checking the actual files that implement each stage.

Run: python -m pytest tests/test_pipeline.py -v
"""

import json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / ".opencode" / "skills"
AGENTS = ROOT / ".opencode" / "agents"
TOOLS = ROOT / ".opencode" / "tools"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


class TestPipelineStages:
    """Every pipeline stage must have an implementing file with key sections."""

    def test_prepare_stage_exists(self):
        """prepare skill is the gate — must have input validation."""
        content = read(SKILLS / "prepare" / "SKILL.md")
        assert "Input Validation" in content, "prepare missing Input Validation"
        assert "HOLD" in content and "PASS" in content, (
            "prepare missing decision outputs"
        )

    def test_orchestrate_stage_exists(self):
        """orchestrate skill drives the flow — must have fan-out + verify gate."""
        content = read(SKILLS / "orchestrate" / "SKILL.md")
        assert "Fan-Out" in content, "orchestrate missing Fan-Out"
        assert "Verify" in content, "orchestrate missing Verify"
        assert "Brief Executor" in content, "orchestrate missing Brief Executor"

    def test_implement_stage_exists(self):
        """implement skill is the executor — must have verify requirement."""
        content = read(SKILLS / "implement" / "SKILL.md")
        assert "Verify" in content, "implement missing Verify"
        assert "KISS" in content, "implement missing KISS principle"

    def test_research_review_parallel(self):
        """researcher + reviewer are parallel lanes — both must be read-only."""
        for agent in ("researcher", "reviewer"):
            content = read(AGENTS / f"{agent}.md")
            assert "Read-only" in content or "read-only" in content.lower(), (
                f"{agent} must be read-only"
            )

    def test_agents_have_output_format(self):
        """Every agent must define its output format (report stage)."""
        for agent in ("orchestrator", "researcher", "reviewer", "executor"):
            content = read(AGENTS / f"{agent}.md")
            assert "Output" in content, f"{agent} missing Output section"


class TestVerifyToolIntegration:
    """The verify custom tool (verify.ts → verify.py) must accept all 3 stages."""

    def test_verify_py_supports_all_stages(self):
        content = read(TOOLS / "verify.py")
        for stage in ("research", "review", "implement"):
            assert f'stage == "{stage}"' in content, f"verify.py missing stage {stage}"

    def test_verify_py_rejects_unknown_stage(self):
        content = read(TOOLS / "verify.py")
        assert "Unknown" in content, "verify.py missing unknown-stage rejection"

    def test_verify_py_has_safe_path_check(self):
        """Path traversal protection must exist (security gate)."""
        content = read(TOOLS / "verify.py")
        assert "is_relative_to" in content or "startswith" in content, (
            "verify.py missing path containment check"
        )


class TestFeedbackLoop:
    """Feedback loop must be wired: learn tool + orchestrator trigger."""

    def test_learn_tool_exists(self):
        assert (TOOLS / "learn.ts").exists(), "learn.ts missing"
        content = read(TOOLS / "learn.ts")
        assert "Farewell-Knowlage" in content, "learn.ts must write to lessons vault"

    def test_orchestrator_has_feedback_trigger(self):
        content = read(AGENTS / "orchestrator.md")
        assert "Feedback" in content, "orchestrator missing Feedback Loop section"
        assert "learn" in content.lower(), "orchestrator must call learn tool"
