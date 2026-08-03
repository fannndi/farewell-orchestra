"""
Tests for profiles/generate.py — validate registry, agent config, model collection.
Run:  python -m pytest tests/ -v
"""
import json, os, sys, tempfile

# Ensure profiles/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "profiles"))
from generate import (
    load_profiles,
    validate_registry,
    find_profile,
    build_agent_config,
    collect_models,
    short_model_id,
    AGENT_TEMPLATES,
)

FIXTURE = os.path.join(os.path.dirname(__file__), "..", "profiles", "profiles.json")


# ── Fixtures ────────────────────────────────────────────────────────────

def get_registry():
    return load_profiles()


# ── Tests ───────────────────────────────────────────────────────────────

class TestLoadProfiles:
    def test_loads_valid_json(self):
        reg = get_registry()
        assert "profiles" in reg
        assert "models" in reg
        assert len(reg["profiles"]) > 0

    def test_has_required_fields_per_profile(self):
        reg = get_registry()
        for p in reg["profiles"]:
            assert "name" in p, f"Profile missing name: {p}"
            assert "label" in p, f"Profile missing label: {p}"
            assert "model" in p, f"Profile missing model: {p}"
            assert "small_model" in p, f"Profile missing small_model: {p}"
            assert "agents" in p, f"Profile missing agents: {p}"
            for role in ("orchestrator", "researcher", "reviewer", "executor"):
                assert role in p["agents"], f"Profile '{p['name']}' missing agent '{role}'"

    def test_models_have_required_keys(self):
        reg = get_registry()
        for mid, cfg in reg["models"].items():
            assert "reasoning" in cfg, f"Model '{mid}' missing reasoning"
            assert "tool_call" in cfg, f"Model '{mid}' missing tool_call"
            assert "limit" in cfg, f"Model '{mid}' missing limit"


class TestValidateRegistry:
    def test_valid_registry_returns_empty_errors(self):
        reg = get_registry()
        errors = validate_registry(reg)
        clean = [e for e in errors if not e.startswith("[WARN]")]  # warnings are ok
        assert len(clean) == 0, f"Validation errors: {clean}"

    def test_detects_duplicate_names(self):
        reg = get_registry()
        reg["profiles"].append(dict(reg["profiles"][0]))  # duplicate first
        errors = validate_registry(reg)
        dup = [e for e in errors if "Duplicate" in e]
        assert len(dup) > 0


class TestFindProfile:
    def test_finds_by_name(self):
        reg = get_registry()
        p = find_profile(reg, "default")
        assert p is not None
        assert p["name"] == "default"

    def test_returns_none_for_missing(self):
        reg = get_registry()
        p = find_profile(reg, "nonexistent-profile")
        assert p is None


class TestBuildAgentConfig:
    def test_returns_all_templates(self):
        reg = get_registry()
        profile = find_profile(reg, "default")
        agents = build_agent_config(profile)
        for name in ("orchestrator", "researcher", "reviewer", "executor"):
            assert name in agents, f"Missing agent '{name}'"
            assert agents[name]["mode"] == ("primary" if name == "orchestrator" else "subagent")

    def test_agents_have_model_assigned(self):
        reg = get_registry()
        profile = find_profile(reg, "default")
        agents = build_agent_config(profile)
        for name in ("orchestrator", "researcher", "reviewer", "executor"):
            assert agents[name].get("model"), f"Agent '{name}' has no model"
            assert "9router/" in agents[name]["model"], f"Agent '{name}' model missing provider prefix"

    def test_hidden_agents_exist(self):
        reg = get_registry()
        profile = find_profile(reg, "default")
        agents = build_agent_config(profile)
        for hidden in ("title", "summary", "compaction"):
            assert hidden in agents, f"Missing hidden agent '{hidden}'"

    def test_disabled_agents_exist(self):
        reg = get_registry()
        profile = find_profile(reg, "default")
        agents = build_agent_config(profile)
        for disabled in ("build", "plan", "general", "explore"):
            assert disabled in agents, f"Missing disabled agent '{disabled}'"
            assert agents[disabled].get("disable") == True


class TestCollectModels:
    def test_deduplicates(self):
        reg = get_registry()
        profile = find_profile(reg, "default")
        models = collect_models(reg, profile)
        # Should have at least orchestrator model + small_model distinct models
        main = profile["model"]
        small = profile["small_model"]
        assert main in models, f"Main model '{main}' not collected"
        assert small in models, f"Small model '{small}' not collected"

    def test_all_profiles_have_valid_model_refs(self):
        reg = get_registry()
        for p in reg["profiles"]:
            models = collect_models(reg, p)
            for m in models:
                assert m in reg["models"], f"Profile '{p['name']}' refs unknown model '{m}'"


class TestShortModelId:
    def test_strips_provider_prefix(self):
        assert short_model_id("9router/ocg/deepseek-v4-flash") == "ocg/deepseek-v4-flash"
        assert short_model_id("9router/oc/north-mini-code-free") == "oc/north-mini-code-free"

    def test_passthrough_without_prefix(self):
        assert short_model_id("ocg/deepseek-v4-flash") == "ocg/deepseek-v4-flash"


# ── Integration Smoke ───────────────────────────────────────────────────

class TestGenerateSmoke:
    """Quick smoke tests — gaya live, bukan mock."""

    def test_generate_default_stdout_produces_json(self):
        """--stdout default should produce valid JSON with proper keys."""
        import subprocess
        script = os.path.join(os.path.dirname(__file__), "..", "profiles", "generate.py")
        result = subprocess.run(
            [sys.executable, script, "--stdout", "default"],
            capture_output=True, text=True, timeout=30
        )
        assert result.returncode == 0, f"STDERR: {result.stderr}"
        # Strip header comment before parsing
        raw = result.stdout
        json_start = raw.index("{")
        parsed = json.loads(raw[json_start:])
        assert "model" in parsed
        assert "agent" in parsed
        assert "orchestrator" in parsed["agent"]
        assert parsed["agent"]["orchestrator"]["model"].startswith("9router/")

    def test_validate_exit_0(self):
        """--validate should exit 0 for current profiles.json."""
        import subprocess
        script = os.path.join(os.path.dirname(__file__), "..", "profiles", "generate.py")
        result = subprocess.run(
            [sys.executable, script, "--validate"],
            capture_output=True, text=True, timeout=30
        )
        assert result.returncode == 0, f"STDERR: {result.stderr}"
        assert "OK" in result.stdout

    def test_generate_nonexistent_profile_fails(self):
        """Generating a nonexistent profile should exit non-zero."""
        import subprocess
        script = os.path.join(os.path.dirname(__file__), "..", "profiles", "generate.py")
        result = subprocess.run(
            [sys.executable, script, "i-dont-exist"],
            capture_output=True, text=True, timeout=30
        )
        assert result.returncode != 0
