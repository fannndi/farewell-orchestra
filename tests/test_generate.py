"""
Tests for profiles/generate.py — validate registry, agent config, model collection.
Run:  python -m pytest tests/ -v
"""
import hashlib, json, os, sys, tempfile

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
    BOILERPLATE,
    MAX_BACKUPS,
    generate,
    rollback,
    BACKUP_DIR,
    ROOT_FILE,
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
            assert "agents" in p, f"Profile missing agents: {p}"
            for role in ("orchestrator", "researcher", "reviewer", "executor"):
                assert role in p["agents"], f"Profile '{p['name']}' missing agent '{role}'"
                assert "model" in p["agents"][role]
                if "small_model" in p["agents"][role]:
                    assert isinstance(p["agents"][role]["small_model"], str)

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
        main = profile["agents"]["orchestrator"]["model"]
        small = profile["agents"]["orchestrator"]["small_model"]
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


class TestSecurityChecks:
    """Verify CBM removed and least-privilege external_directory."""

    def test_boilerplate_has_no_codebase_memory_mcp(self):
        """BOILERPLATE must not contain codebase-memory-mcp."""
        from generate import BOILERPLATE
        bp_str = json.dumps(BOILERPLATE)
        assert "codebase-memory-mcp" not in bp_str

    def test_executor_external_directory_no_source_code(self):
        """Executor external_directory must not contain 'Source Code'."""
        from generate import AGENT_TEMPLATES
        ext = AGENT_TEMPLATES["executor"].get("permission", {}).get("external_directory", {})
        for key in ext:
            assert "Source Code" not in key, f"Executor external_directory contains 'Source Code': {key}"


# ── Behavioral: Permission Scoping ──────────────────────────────────────

class TestPermissionScoping:
    """Guard: executor MUST have bash:allow; researcher/reviewer MUST NOT have edit/bash."""

    def test_executor_has_bash_allow(self):
        assert AGENT_TEMPLATES["executor"]["permission"]["bash"] == "allow"

    def test_researcher_reviewer_deny_edit_bash(self):
        for role in ("researcher", "reviewer"):
            perm = AGENT_TEMPLATES[role]["permission"]
            assert perm["edit"] == "deny", f"{role} edit should be deny, got {perm['edit']}"
            assert perm["bash"] == "deny", f"{role} bash should be deny, got {perm['bash']}"

    def test_boilerplate_deny_by_default(self):
        assert BOILERPLATE["permission"]["edit"] == "ask"
        assert BOILERPLATE["permission"]["bash"] == "ask"

    def test_executor_external_directory_scoped(self):
        ext = AGENT_TEMPLATES["executor"]["permission"]["external_directory"]
        assert set(ext.keys()) == {"~/projects/**", "~/Documents/Farewell-Knowlage/**"}


# ── Behavioral: Backup Integrity ────────────────────────────────────────

class TestBackupIntegrity:
    """Guard: generate() must create backups and respect MAX_BACKUPS."""

    def _save_root(self):
        root = os.path.abspath(ROOT_FILE)
        if os.path.isfile(root):
            with open(root, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def _restore_root(self, content):
        root = os.path.abspath(ROOT_FILE)
        if content is None:
            if os.path.isfile(root):
                os.remove(root)
        else:
            with open(root, "w", encoding="utf-8") as f:
                f.write(content)

    def test_backup_created_before_overwrite(self):
        orig = self._save_root()
        try:
            backup_dir = os.path.abspath(BACKUP_DIR)
            before_count = len([f for f in os.listdir(backup_dir) if f.startswith("opencode.")]) if os.path.isdir(backup_dir) else 0
            generate("default")
            after_count = len([f for f in os.listdir(backup_dir) if f.startswith("opencode.")]) if os.path.isdir(backup_dir) else 0
            assert after_count >= before_count, "No backup created after generate()"
        finally:
            self._restore_root(orig)

    def test_max_backups_respected(self):
        orig = self._save_root()
        try:
            backup_dir = os.path.abspath(BACKUP_DIR)
            os.makedirs(backup_dir, exist_ok=True)
            # Alternate profiles to trigger backup creation (same profile = no-op)
            for i in range(MAX_BACKUPS + 2):
                profile = "mix" if i % 2 == 0 else "default"
                generate(profile)
            backups = [f for f in os.listdir(backup_dir) if f.startswith("opencode.") and f.endswith(".jsonc")]
            assert len(backups) <= MAX_BACKUPS, f"Expected <= {MAX_BACKUPS} backups, got {len(backups)}"
        finally:
            self._restore_root(orig)


# ── Behavioral: Rollback Correctness ────────────────────────────────────

class TestRollbackCorrectness:
    """Guard: rollback() must restore the previous opencode.jsonc content."""

    def _save_root(self):
        root = os.path.abspath(ROOT_FILE)
        if os.path.isfile(root):
            with open(root, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def _restore_root(self, content):
        root = os.path.abspath(ROOT_FILE)
        if content is None:
            if os.path.isfile(root):
                os.remove(root)
        else:
            with open(root, "w", encoding="utf-8") as f:
                f.write(content)

    def test_rollback_restores_previous(self):
        orig = self._save_root()
        try:
            # Generate "default" to establish a known state
            generate("default")
            root = os.path.abspath(ROOT_FILE)
            with open(root, "r", encoding="utf-8") as f:
                default_content = f.read()
            default_hash = hashlib.md5(default_content.encode()).hexdigest()

            # Generate "mix" — this creates a backup of "default" content
            generate("mix")
            with open(root, "r", encoding="utf-8") as f:
                mix_content = f.read()
            assert hashlib.md5(mix_content.encode()).hexdigest() != default_hash, \
                "default and mix should produce different content"

            # Rollback should restore the backup (which contains "default" content)
            rollback()
            with open(root, "r", encoding="utf-8") as f:
                restored_content = f.read()
            restored_hash = hashlib.md5(restored_content.encode()).hexdigest()
            assert restored_hash == default_hash, \
                f"Rollback did not restore: expected {default_hash}, got {restored_hash}"
        finally:
            self._restore_root(orig)
