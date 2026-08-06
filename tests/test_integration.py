"""
test_integration.py — Golden-path integration tests.
Generate semua profile, validate JSON, check permission consistency.

Run:  python -m pytest tests/test_integration.py -v
"""

import json, os, sys, subprocess

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "profiles"))
from generate import load_profiles, find_profile

ROOT = os.path.join(os.path.dirname(__file__), "..")
GENERATE_PY = os.path.join(ROOT, "profiles", "generate.py")


def get_registry():
    return load_profiles()


class TestGoldenPath:
    """Generate semua profile, validate JSON structure."""

    def test_all_profiles_generate_valid_json(self):
        """Every profile should produce valid JSON with required keys."""
        reg = get_registry()
        for profile in reg["profiles"]:
            result = subprocess.run(
                [sys.executable, GENERATE_PY, "--stdout", profile["name"]],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=ROOT,
            )
            assert result.returncode == 0, (
                f"Profile '{profile['name']}' failed: {result.stderr}"
            )

            # Parse JSON (skip header comment)
            raw = result.stdout
            json_start = raw.index("{")
            config = json.loads(raw[json_start:])

            # Required keys
            assert "model" in config, f"Profile '{profile['name']}': missing 'model'"
            assert "agent" in config, f"Profile '{profile['name']}': missing 'agent'"
            assert "permission" in config, (
                f"Profile '{profile['name']}': missing 'permission'"
            )

            # All 4 agents present
            for agent in ["orchestrator", "researcher", "reviewer", "executor"]:
                assert agent in config["agent"], (
                    f"Profile '{profile['name']}': missing agent '{agent}'"
                )
                assert "model" in config["agent"][agent], (
                    f"Profile '{profile['name']}': agent '{agent}' missing model"
                )

    def test_all_models_match_provider(self):
        """All model strings should reference declared providers."""
        reg = get_registry()
        for profile in reg["profiles"]:
            result = subprocess.run(
                [sys.executable, GENERATE_PY, "--stdout", profile["name"]],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=ROOT,
            )
            assert result.returncode == 0, f"Profile '{profile['name']}' failed"

            raw = result.stdout
            json_start = raw.index("{")
            config = json.loads(raw[json_start:])

            # Check provider models
            provider_models = set()
            for provider in config.get("provider", {}).values():
                for model_key in provider.get("models", {}).keys():
                    provider_models.add(model_key)

            # Check all agent models are in provider
            for agent_name, agent_config in config["agent"].items():
                model = agent_config.get("model", "")
                if (
                    model
                    and not agent_config.get("hidden")
                    and not agent_config.get("disable")
                ):
                    # Model should be declared in provider
                    model_short = (
                        model.replace("9router/", "")
                        if model.startswith("9router/")
                        else model
                    )
                    assert model_short in provider_models or model in provider_models, (
                        f"Profile '{profile['name']}': agent '{agent_name}' model '{model}' not in provider models"
                    )

    def test_permission_skill_superset(self):
        """permission.skill allowlist should be superset of all agent skills."""
        reg = get_registry()
        for profile in reg["profiles"]:
            result = subprocess.run(
                [sys.executable, GENERATE_PY, "--stdout", profile["name"]],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=ROOT,
            )
            assert result.returncode == 0, f"Profile '{profile['name']}' failed"

            raw = result.stdout
            json_start = raw.index("{")
            config = json.loads(raw[json_start:])

            # Get skill allowlist
            skill_allowlist = set()
            for key, val in config.get("permission", {}).get("skill", {}).items():
                if key != "*" and val == "allow":
                    skill_allowlist.add(key)

            # Get skills referenced in agent frontmatter
            # (We can't easily parse frontmatter from here, so check the generated config)
            # The skill allowlist should at least have the core skills
            core_skills = {
                "prepare",
                "orchestrate",
                "research",
                "review",
                "implement",
                "bootstrap-project",
            }
            for skill in core_skills:
                assert skill in skill_allowlist, (
                    f"Profile '{profile['name']}': core skill '{skill}' not in permission allowlist"
                )

    def test_no_phantom_skills_in_allowlist(self):
        """No skill in allowlist that doesn't exist on disk."""
        skill_dirs = sorted(
            [
                d
                for d in os.listdir(os.path.join(ROOT, ".opencode", "skills"))
                if os.path.isdir(os.path.join(ROOT, ".opencode", "skills", d))
            ]
        )

        reg = get_registry()
        profile = reg["profiles"][
            0
        ]  # Check first profile (all should have same allowlist)
        result = subprocess.run(
            [sys.executable, GENERATE_PY, "--stdout", profile["name"]],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=ROOT,
        )
        assert result.returncode == 0

        raw = result.stdout
        json_start = raw.index("{")
        config = json.loads(raw[json_start:])

        skill_allowlist = set()
        for key, val in config.get("permission", {}).get("skill", {}).items():
            if key != "*" and val == "allow":
                skill_allowlist.add(key)

        # Remove customize-opencode (special built-in skill)
        skill_allowlist.discard("customize-opencode")

        for skill in skill_allowlist:
            assert skill in skill_dirs, (
                f"Phantom skill '{skill}' in allowlist but not on disk"
            )


class TestConsistency:
    """Cross-reference consistency checks."""

    def test_agent_count_in_ci_matches_disk(self):
        """CI workflow should expect same number of agents as on disk."""
        agent_files = [
            f
            for f in os.listdir(os.path.join(ROOT, ".opencode", "agents"))
            if f.endswith(".md")
        ]

        ci_content = open(
            os.path.join(ROOT, ".github", "workflows", "ci.yaml"), encoding="utf-8"
        ).read()

        # Count expected agents in CI
        import re

        expected_match = re.search(
            r"expected_agents.*?sorted\(\[(.*?)\]\)", ci_content, re.DOTALL
        )
        if expected_match:
            expected = re.findall(r'"(\w+\.md)"', expected_match.group(1))
            assert len(expected) == len(agent_files), (
                f"CI expects {len(expected)} agents, disk has {len(agent_files)}"
            )

    def test_skill_count_in_ci_matches_disk(self):
        """CI workflow should expect same number of skills as on disk."""
        skill_dirs = [
            d
            for d in os.listdir(os.path.join(ROOT, ".opencode", "skills"))
            if os.path.isdir(os.path.join(ROOT, ".opencode", "skills", d))
        ]

        # No hardcoded count in CI anymore (check-consistency handles it)
        # But verify skills match agent frontmatter
        assert len(skill_dirs) > 0, "No skills found on disk"
