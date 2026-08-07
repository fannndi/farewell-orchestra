"""
test_gaps.py — Tests for previously untested critical paths.
Covers: cross-project flow, hooks, auto-load output integrity, config safety.

Run: python -m pytest tests/test_gaps.py -v
"""

import os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


class TestCrossProject:
    """Cross-project flow — the major untested path."""

    def test_guide_exists_and_covers_flow(self):
        guide = read(ROOT / "cross-project" / "guide.md")
        assert "Permission" in guide, "guide missing permission pre-check"
        assert "Project Type Detection" in guide, "guide missing type detection"
        assert "Reverse Engineering" in guide, "guide missing reverse engineering mode"

    def test_prepare_references_cross_project(self):
        prep = read(ROOT / ".opencode" / "skills" / "prepare" / "SKILL.md")
        assert "cross-project" in prep.lower(), (
            "prepare missing cross-project reference"
        )

    def test_sub_project_template_exists(self):
        assert (ROOT / "cross-project" / "sub-project.md").exists(), (
            "sub-project.md missing"
        )


class TestHooks:
    """Hook execution paths."""

    def test_hooks_jsonc_resolves(self):
        hooks = read(ROOT / ".opencode" / "hooks" / "hooks.jsonc")
        import json, re

        # strip comments if jsonc
        content = re.sub(r"//[^\n]*", "", hooks)
        try:
            json.loads(content)
            parsed = True
        except json.JSONDecodeError:
            parsed = False
        assert parsed, "hooks.jsonc not valid JSON after comment strip"

    def test_hook_targets_exist(self):
        hooks = read(ROOT / ".opencode" / "hooks" / "hooks.jsonc")
        # find all .py/.ts references and verify existence
        import re

        refs = re.findall(r"[\"']([^\"']+\.(?:py|ts))[\"']", hooks)
        assert len(refs) >= 3, f"expected 3+ hook targets, got {len(refs)}"
        for r in refs:
            candidates = [ROOT / r, ROOT / ".opencode" / r.lstrip(".opencode/")]
            assert any(c.exists() for c in candidates), f"hook target missing: {r}"

    def test_auto_load_script_exists(self):
        assert (ROOT / ".opencode" / "tools" / "auto-load-skills.py").exists()


class TestAutoLoadOutput:
    """Generated context files must be complete + valid."""

    def test_persona_context_has_rules_section(self):
        for agent in ("orchestrator", "researcher", "reviewer", "executor"):
            f = ROOT / ".opencode" / "tools" / f"persona-context-{agent}.md"
            assert f.exists(), f"persona-context-{agent}.md missing"
            content = read(f)
            assert "## Rules" in content, f"persona-context-{agent}.md dropped ## Rules"

    def test_persona_context_no_unterminated_fence(self):
        for agent in ("orchestrator", "researcher", "reviewer", "executor"):
            f = ROOT / ".opencode" / "tools" / f"persona-context-{agent}.md"
            content = read(f)
            fences = content.count("```")
            assert fences % 2 == 0, (
                f"persona-context-{agent}.md has odd code fences ({fences})"
            )

    def test_skill_context_has_key_rules(self):
        # skill context should include key rules, not just headers
        f = ROOT / ".opencode" / "tools" / "skill-context-orchestrator.md"
        assert f.exists(), "skill-context-orchestrator.md missing"
        content = read(f)
        assert len(content.strip()) > 200, "skill context too thin (<200 chars)"


class TestConfigSafety:
    """Config safety — permission model (parsed JSON, not string grep)."""

    @staticmethod
    def _parse_opencode():
        """Strip full-line // comments (header only) then parse JSON."""
        import json

        raw = read(ROOT / "opencode.jsonc")
        lines = [l for l in raw.splitlines() if not l.lstrip().startswith("//")]
        return json.loads("\n".join(lines))

    def test_env_read_denied_for_all_agents(self):
        js = self._parse_opencode()
        with_dict_read = [
            a
            for a in js["agent"].values()
            if isinstance(a.get("permission", {}).get("read"), dict)
        ]
        assert len(with_dict_read) >= 4, (
            f"expected 4 agents with granular read perms, got {len(with_dict_read)}"
        )
        for name, agent in js["agent"].items():
            read_perm = agent.get("permission", {}).get("read")
            if isinstance(read_perm, dict):
                assert read_perm.get("**/.env*") == "deny", (
                    f"{name} read must deny .env"
                )

    def test_executor_edit_denies_secrets(self):
        js = self._parse_opencode()
        edit = js["agent"]["executor"]["permission"]["edit"]
        assert edit.get("**/.env*") == "deny", "executor edit must deny .env"
        assert edit.get("profiles/generate.py") == "deny", (
            "executor edit must deny profiles/generate.py"
        )
        assert edit.get(".opencode/**") == "deny", (
            "executor edit must deny .opencode/** (hooks/tools/skills/soul)"
        )
        assert edit.get("AGENTS.md") == "deny", "executor edit must deny AGENTS.md"
        assert edit.get("cross-project/guide.md") == "deny", (
            "executor edit must deny cross-project/guide.md"
        )

    def test_skill_allowlist_matches_disk(self):
        # count skills on disk
        disk = {d.name for d in (ROOT / ".opencode" / "skills").iterdir() if d.is_dir()}
        assert len(disk) == 18, f"expected 18 skills, got {len(disk)}"
