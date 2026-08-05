"""
Profile generator for opencode.jsonc
Usage:  python profiles/generate.py <profile-name> [--stdout]
          python profiles/generate.py Pro
          python profiles/generate.py "Eco" --stdout > opencode.jsonc

Reads profiles.json, generates full opencode.jsonc with correct model assignments.
"""

import json
import os
import sys
import time

PROFILES_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_JSON = os.path.join(PROFILES_DIR, "profiles.json")
TEMP_FILE = os.path.join(PROFILES_DIR, "opencode.temp.jsonc")
ROOT_FILE = os.path.join(PROFILES_DIR, "..", "opencode.jsonc")
BACKUP_DIR = os.path.join(PROFILES_DIR, "backups")
MAX_BACKUPS = 3

# ── boilerplate (shared across all profiles) ──────────────────────────

BOILERPLATE = {
    "$schema": "https://opencode.ai/config.json",
    "default_agent": "orchestrator",
    "instructions": ["AGENTS.md"],
    "subagent_depth": 2,
    "share": "disabled",
    "permission": {
        "doom_loop": "deny",
        "edit": "ask",
        "bash": "ask",
        "task": "ask",
        "webfetch": "ask",
        "websearch": "ask",
        "read": "allow",
        "glob": "allow",
        "grep": "allow",
        "list": "allow",
        "question": "allow",
        "todowrite": "allow",
        "lsp": "allow",
        "mcp_*": "deny",
        "skill": {
            "*": "deny",
            "anti-gigo": "allow",
            "bootstrap-project": "allow",
            "customize-opencode": "allow",
            "forensic": "allow",
            "grill": "allow",
            "minimal-impl": "allow",
            "orchestrate": "allow",
            "stride-audit": "allow",
            "synthesis-brief": "allow",
            "task-chunking": "allow",
            "verification-ground-truth": "allow",
            "web-research": "allow",
        },
    },
    "references": {
        "projects": {"path": "~/projects", "description": "Folder project Boss"},
        "opencode-sdk": {
            "repository": "anomalyco/opencode-sdk-js",
            "description": "OpenCode SDK",
        },
        "opencode-config": {
            "path": "~/.config/opencode",
            "description": "OpenCode global config",
            "hidden": True,
        },
    },
    "autoupdate": "notify",
    "theme": "dark",
    "username": "farewell-orchestra",
    "provider": {
        "9router": {
            "name": "9Router Gateway",
            "npm": "@ai-sdk/openai-compatible",
            "env": ["NINEROUTER_API_KEY"],
            "options": {
                "baseURL": "http://127.0.0.1:20128/v1",
                "apiKey": "{env:NINEROUTER_API_KEY}",
                "setCacheKey": True,
                "timeout": 300000,
                "headerTimeout": 90000,
                "chunkTimeout": 120000,
            },
        }
    },
    "experimental": {
        "primary_tools": ["todowrite", "question"],
        "policies": [
            {"effect": "deny", "action": "provider.use", "resource": "*"},
            {"effect": "allow", "action": "provider.use", "resource": "9router"},
        ],
    },
    "tool_output": {"max_lines": 1000, "max_bytes": 20000},
    "compaction": {
        "auto": True,
        "preserve_recent_tokens": 4000,
        "reserved": 14000,
        "prune": True,
        "prune_rules": {
            "tool_output": {
                "min_chars": 500,
                "keep_head_pct": 0.2,
                "keep_tail_pct": 0.3,
            },
            "file_lists": {"collapse_to": "first_5_and_last_2"},
        },
    },
    "watcher": {
        "ignore": [
            ".git/**",
            "node_modules/**",
            "dist/**",
            "build/**",
            ".next/**",
            ".venv/**",
            "venv/**",
            "__pycache__/**",
            ".pytest_cache/**",
        ]
    },
    "attachment": {
        "image": {
            "auto_resize": True,
            "max_width": 2000,
            "max_height": 2000,
            "max_base64_bytes": 5242880,
        }
    },
    "lsp": False,
    "formatter": True,
}

# Agent config template — only `model` changes per profile
# external_directory scoped ke ~/projects/** — least privilege. JANGAN tambah ~/Documents/** (private files).
AGENT_TEMPLATES = {
    "orchestrator": {
        "color": "#7c3aed",
        "description": "Workflow orchestrator",
        "mode": "primary",
        "request": {"body": {"temperature": 0.2}},
        "steps": 500,
        "prompt": "Orchestrator: decompose -> fan-out parallel via `task` tool -> synthesize -> brief executor. Trust your sub-agents (researcher/reviewer/executor) to do their job. USE task tool with subagent_type for every non-trivial request. WAJIB parallel dispatch researcher+reviewer before executor. WAJIB: load skill tool via `skill` — anti-gigo + orchestrate di awal session/request.",
        "permission": {
            "read": {"*.md": "allow", "*": "ask"},
            "edit": {
                "sub-project.md": "allow",
                "Farewell-Knowlage/Lessons.md": "deny",
                "*.md": "deny",
                "*": "deny",
            },
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "question": "allow",
            "skill": "allow",
            "todowrite": "allow",
            "lsp": "allow",
            "external_directory": {"~/projects/**": "allow"},
            "task": {
                "*": "deny",
                "researcher": "allow",
                "reviewer": "allow",
                "executor": "allow",
            },
        },
    },
    "researcher": {
        "color": "#3b82f6",
        "description": "Read-only researcher",
        "mode": "subagent",
        "request": {"body": {"temperature": 0.1}},
        "steps": 400,
        "prompt": "Read-only investigator. Return evidence file:line. Be thorough — orchestrator trusts you. Use forensic skill for code, web-research for external. WAJIB: di awal task, load skill tool via `skill` — forensic untuk codebase, web-research untuk external. Jangan mulai kerja sebelum skill di-load.",
        "permission": {
            "*": "deny",
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "webfetch": "allow",
            "websearch": "allow",
            "lsp": "allow",
            "skill": "allow",
            "edit": "deny",
            "bash": "deny",
            "external_directory": {"~/projects/**": "allow"},
            "task": "deny",
        },
    },
    "reviewer": {
        "color": "#f59e0b",
        "description": "Read-only reviewer",
        "mode": "subagent",
        "request": {"body": {"temperature": 0.1}},
        "steps": 400,
        "prompt": "Read-only auditor. STRIDE analysis. Return [BLOCKING]/[SHOULD]/[NICE] with file:line. Be harsh — orchestrator needs your skepticism. WAJIB: di awal task, load skill tool via `skill` — stride-audit. Jangan mulai audit sebelum skill di-load.",
        "permission": {
            "*": "deny",
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "webfetch": "allow",
            "websearch": "allow",
            "lsp": "allow",
            "skill": "allow",
            "edit": "deny",
            "bash": "deny",
            "external_directory": {"~/projects/**": "allow"},
            "task": "deny",
        },
    },
    "executor": {
        "color": "#10b981",
        "description": "Implementation worker",
        "mode": "subagent",
        "request": {"body": {"temperature": 0.2}},
        "steps": 500,
        "prompt": "Implement precisely per brief. YAGNI. One change per edit. Verify before report. You have edit access — use it. Trusted to execute autonomously. WAJIB: di awal task, load skill tool via `skill` — minimal-impl sebelum nulis kode, verification-ground-truth sebelum report.",
        "permission": {
            "read": "allow",
            "edit": "allow",
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "bash": {
                "git status": "allow",
                "git diff": "allow",
                "git log": "allow",
                "git show": "allow",
                "npm test": "allow",
                "npm run build": "allow",
                "npm run lint": "allow",
                "*": "ask",
            },
            "lsp": "allow",
            "skill": "allow",
            "external_directory": {"~/projects/**": "allow"},
            "task": "deny",
        },
    },
}

DISABLED_AGENTS = {
    "build": {
        "mode": "primary",
        "color": "primary",
        "disable": True,
        "permission": {
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "edit": "deny",
            "bash": "deny",
            "task": "deny",
        },
    },
    "plan": {
        "mode": "primary",
        "color": "secondary",
        "disable": True,
        "permission": {
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "edit": "deny",
            "bash": "deny",
            "task": "deny",
        },
    },
    "general": {
        "mode": "subagent",
        "disable": True,
        "permission": {
            "*": "deny",
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "task": "deny",
        },
    },
    "explore": {
        "mode": "subagent",
        "disable": True,
        "permission": {
            "*": "deny",
            "read": "allow",
            "glob": "allow",
            "grep": "allow",
            "list": "allow",
            "task": "deny",
        },
    },
}


def load_profiles():
    try:
        with open(PROFILES_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {PROFILES_JSON}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in {PROFILES_JSON}: {e}", file=sys.stderr)
        sys.exit(1)


def find_profile(registry, name):
    for p in registry["profiles"]:
        if p["name"] == name:
            return p
    return None


def collect_models(registry, profile):
    """Collect all unique model IDs used in this profile."""
    models = set()
    for agent_name, agent_data in profile.get("agents", {}).items():
        if isinstance(agent_data, dict):
            models.add(agent_data.get("model", ""))
            models.add(agent_data.get("small_model", ""))
        else:
            # legacy: agent_data is a plain model string
            models.add(agent_data)
    models.discard("")
    return models


def build_agent_config(profile):
    """Build the agent section with correct models per profile."""
    agents = {}
    for name, template in AGENT_TEMPLATES.items():
        cfg = dict(template)
        agent_data = profile["agents"].get(name)
        if isinstance(agent_data, dict):
            cfg["model"] = agent_data["model"]
            if agent_data.get("small_model"):
                cfg["small_model"] = agent_data["small_model"]
        else:
            # legacy: agent_data is a plain model string
            cfg["model"] = agent_data
        agents[name] = cfg

    # Hidden agents use orchestrator's small_model as fallback
    orch = profile["agents"].get("orchestrator", {})
    if isinstance(orch, dict):
        small = orch.get("small_model", orch.get("model", ""))
    else:
        small = orch
    hidden = {
        "title": {
            "model": small,
            "mode": "primary",
            "hidden": True,
            "permission": {
                "read": "allow",
                "glob": "allow",
                "grep": "allow",
                "list": "allow",
                "edit": "deny",
                "bash": "deny",
                "task": "deny",
            },
        },
        "summary": {
            "model": small,
            "mode": "primary",
            "hidden": True,
            "permission": {
                "read": "allow",
                "glob": "allow",
                "grep": "allow",
                "list": "allow",
                "edit": "deny",
                "bash": "deny",
                "task": "deny",
            },
        },
        "compaction": {
            "model": small,
            "mode": "primary",
            "hidden": True,
            "steps": 8,
            "permission": {
                "read": "allow",
                "glob": "allow",
                "grep": "allow",
                "list": "allow",
                "edit": "deny",
                "bash": "deny",
                "task": "deny",
            },
        },
    }
    agents.update(hidden)
    agents.update(DISABLED_AGENTS)
    return agents


PROVIDER_PREFIX = "9router/"


def short_model_id(full_id):
    """Strip provider prefix for provider.models keys."""
    if full_id.startswith(PROVIDER_PREFIX):
        return full_id[len(PROVIDER_PREFIX) :]
    return full_id


def build_provider_models(registry, profile):
    """Build provider.models section — only models used by this profile."""
    model_ids = collect_models(registry, profile)
    result = {}
    for mid in sorted(model_ids):
        cfg = registry["models"].get(mid)
        if cfg is None:
            print(
                f"[WARN] Model '{mid}' not found in registry.models, using defaults",
                file=sys.stderr,
            )
            cfg = {"reasoning": True, "tool_call": True}
        key = short_model_id(mid)
        result[key] = {
            "name": key,
            "reasoning": cfg.get("reasoning", True),
            "tool_call": cfg.get("tool_call", True),
            "limit": cfg.get("limit", {"context": 128000, "output": 128000}),
        }
    return result


def generate(profile_name, to_stdout=False):
    registry = load_profiles()
    profile = find_profile(registry, profile_name)

    if not profile:
        names = [p["name"] for p in registry["profiles"]]
        print(f"[ERROR] Profile '{profile_name}' not found.", file=sys.stderr)
        print(f"   Available: {', '.join(names)}", file=sys.stderr)
        sys.exit(1)

    config = dict(BOILERPLATE)
    # Top-level model/small_model from orchestrator (default_agent)
    orch = profile["agents"].get("orchestrator", {})
    if isinstance(orch, dict):
        config["model"] = orch["model"]
        if orch.get("small_model"):
            config["small_model"] = orch["small_model"]
    else:
        config["model"] = orch
    config["provider"]["9router"]["models"] = build_provider_models(registry, profile)
    config["agent"] = build_agent_config(profile)

    output = json.dumps(config, indent=2, ensure_ascii=False)
    header = f"// Profile: {profile['label']}\n"

    if to_stdout:
        sys.stdout.write(header + output + "\n")
        return

    # No-op detection: compare header AND content hash
    # Header-only comparison false-positive when BOILERPLATE changes but label stays
    root_path = os.path.abspath(ROOT_FILE)
    if os.path.isfile(root_path):
        try:
            with open(root_path, "r", encoding="utf-8") as f:
                existing_raw = f.read()
            existing_json_start = existing_raw.index("{")
            existing_json = (
                existing_raw[existing_json_start:].strip()
                if existing_json_start >= 0
                else ""
            )
            generated_json = output.strip()
            if existing_json == generated_json:
                print(f"[OK] Already active: {profile['label']} (no change)")
                return
        except Exception:
            pass  # proceed if can't read

    # Write to temp first, then atomically copy to root
    temp_path = os.path.abspath(TEMP_FILE)

    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(header + output + "\n")
    print(f"[OK] Wrote temp: {temp_path}")

    # Validate JSON before replacing the real file
    try:
        with open(temp_path, "r", encoding="utf-8") as f:
            raw = f.read()
            json.loads(raw[raw.index("{") :])
    except Exception as e:
        print(f"[ERROR] Generated file invalid, NOT copying: {e}", file=sys.stderr)
        sys.exit(1)

    import shutil, glob as glob_mod

    # Backup existing opencode.jsonc before overwrite (keep MAX_BACKUPS latest)
    if os.path.isfile(root_path):
        try:
            os.makedirs(BACKUP_DIR, exist_ok=True)
            ts = time.strftime("%Y%m%d-%H%M%S")
            backup_path = os.path.join(BACKUP_DIR, f"opencode.{ts}.jsonc")
            shutil.copy2(root_path, backup_path)
            # Prune old backups
            backups = sorted(
                glob_mod.glob(os.path.join(BACKUP_DIR, "opencode.*.jsonc"))
            )
            while len(backups) > MAX_BACKUPS:
                os.remove(backups.pop(0))
        except Exception as e:
            print(f"[WARN] Backup failed: {e}", file=sys.stderr)

    try:
        shutil.copy2(temp_path, root_path)
    except Exception as e:
        print(f"[ERROR] Failed to copy to {root_path}: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"[OK] Copied -> {root_path}  ({profile['label']})")

    # Auto-regenerate example file (reference only) — avoids manual drift
    if profile_name == registry["profiles"][0]["name"]:
        _example_path = os.path.join(
            os.path.dirname(__file__), "opencode.example.jsonc"
        )
        with open(_example_path, "w", encoding="utf-8") as f:
            f.write(
                f"// Example output — generated by: python profiles/generate.py --stdout {registry['profiles'][0]['name']}\n"
            )
            f.write(
                "// This file is REGENERATED automatically. Do not edit manually.\n"
            )
            f.write("// The actual active config is opencode.jsonc (gitignored).\n")
            f.write(header + output + "\n")


def validate_registry(registry):
    """Validate profiles.json integrity. Return list of errors."""
    errors = []
    seen_names = set()
    models_reg = registry.get("models", {})

    for i, p in enumerate(registry.get("profiles", [])):
        name = p.get("name", f"#{i}")
        # Required fields
        for field in ("name", "label"):
            if field not in p:
                errors.append(f"[ERROR] Profile '{name}' missing field '{field}'")
        # Duplicate names
        if name in seen_names:
            errors.append(f"[ERROR] Duplicate profile name: '{name}'")
        seen_names.add(name)

        # Check agents
        agents = p.get("agents", {})
        if not agents:
            errors.append(f"[ERROR] Profile '{name}' has no agents")
        else:
            for agent_name in AGENT_TEMPLATES:
                agent_data = agents.get(agent_name)
                if isinstance(agent_data, dict):
                    for mk in ("model", "small_model"):
                        mid = agent_data.get(mk)
                        if mid and mid not in models_reg:
                            errors.append(
                                f"[WARN] Profile '{name}' agent '{agent_name}' {mk} '{mid}' not in registry"
                            )
                elif agent_data and agent_data not in models_reg:
                    errors.append(
                        f"[WARN] Profile '{name}' agent '{agent_name}' model '{agent_data}' not in registry"
                    )

    if not registry.get("profiles"):
        errors.append("[WARN] No profiles defined")

    return errors


# ── ANSI colors (Windows 10+ CMD / Windows Terminal) ──────────────
_RESET = "\033[0m"
_BOLD = "\033[1m"
_RED = "\033[31m"
_GREEN = "\033[32m"
_YELLOW = "\033[33m"
_CYAN = "\033[36m"
_MAGENTA = "\033[35m"


def show_menu():
    """Interactive menu — pick a profile, generate."""
    registry = load_profiles()
    profiles = registry["profiles"]

    # detect active profile from opencode.jsonc header comment
    active_label = None
    root_path = os.path.abspath(ROOT_FILE)
    try:
        with open(root_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("// Profile:"):
                    active_label = line.split("// Profile:", 1)[1].strip()
                    break
    except OSError:
        pass

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{_BOLD}{_CYAN}{'=' * 62}{_RESET}")
        print(f"{_BOLD}{_CYAN}  PROFILE SWITCHER - Farewell Orchestra{_RESET}")
        print(f"{_BOLD}{_CYAN}{'=' * 62}{_RESET}")
        for i, p in enumerate(profiles, 1):
            is_active = p["label"] == active_label
            name_color = _GREEN if is_active else _CYAN
            suffix = f" {_GREEN}(AKTIF){_RESET}" if is_active else ""
            print(f"  {_CYAN}{'-' * 62}{_RESET}")
            print(f"  {name_color}{_BOLD}[{i}] {p['name']}{_RESET}{suffix}")
            lbl = p["label"][:60] + ("..." if len(p["label"]) > 60 else "")
            print(f"      {_CYAN}{'Label':<13}{_RESET}: {lbl}")
            for akey, alabel in [
                ("orchestrator", "Orchestrator"),
                ("researcher", "Researcher"),
                ("reviewer", "Reviewer"),
                ("executor", "Executor"),
            ]:
                ad = p["agents"].get(akey)
                if ad is not None:
                    model = ad.get("model", "") if isinstance(ad, dict) else ad
                    small = ad.get("small_model", "") if isinstance(ad, dict) else ""
                    print(f"      {_CYAN}{alabel:<13}{_RESET}: {model}")
                    if small:
                        print(f"      {_CYAN}{'small':<13}{_RESET}: {small}")
        print(f"  {_CYAN}{'-' * 62}{_RESET}")
        print(f"  {_YELLOW}0   Keluar{_RESET}")
        print()

        try:
            choice = input(f"  {_GREEN}Pilihan [0-{len(profiles)}]:{_RESET} ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "0":
            print(f"\n  {_YELLOW}Bye.{_RESET}")
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(profiles):
                profile = profiles[idx]
                print(
                    f"\n  >>> Memilih: {_BOLD}{profile['name']}{_RESET} ({profile['label']})"
                )
                generate(profile["name"])
                input("\n  [Enter] untuk kembali ke menu...")
            else:
                input(f"\n  {_RED}Pilihan {choice} nggak ada. [Enter]...{_RESET}")
        except ValueError:
            input(f"\n  {_RED}'{choice}' bukan angka. [Enter]...{_RESET}")


def rollback():
    """Restore latest backup from profiles/backups/ to opencode.jsonc"""
    import glob, json, shutil

    root_path = os.path.abspath(ROOT_FILE)
    backup_pattern = os.path.join(BACKUP_DIR, "opencode.*.jsonc")
    backups = sorted(glob.glob(backup_pattern), reverse=True)

    if not backups:
        print("[ERROR] No backup found")
        sys.exit(1)

    latest = backups[0]
    print(f"[INFO] Restoring from backup: {os.path.basename(latest)}")

    # Validate JSON before copying (same pattern as generate())
    try:
        with open(latest, "r", encoding="utf-8") as f:
            raw = f.read()
            json.loads(raw[raw.index("{") :])
    except Exception as e:
        print(f"[ERROR] Backup file invalid JSON: {e}")
        sys.exit(1)

    try:
        shutil.copy2(latest, root_path)
    except Exception as e:
        print(f"[ERROR] Failed to copy to {root_path}: {e}")
        sys.exit(1)

    print(f"[OK] Restored from backup: {os.path.basename(latest)}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        registry = load_profiles()
        names = [p["name"] for p in registry["profiles"]]
        print("Usage:")
        print(
            "  python profiles/generate.py <profile-name>     -> generate & copy to opencode.jsonc"
        )
        print("  python profiles/generate.py --menu | -i        -> interactive menu")
        print("  python profiles/generate.py --stdout <name>    -> print to stdout")
        print(
            "  python profiles/generate.py --validate         -> check profiles.json integrity"
        )
        print(
            "  python profiles/generate.py --rollback         -> restore latest backup to opencode.jsonc"
        )
        print(f"\nProfiles: {', '.join(names)}")
        sys.exit(0)

    if args[0] in ("--menu", "-i", "-m"):
        show_menu()
        sys.exit(0)

    if args[0] == "--stdout" and len(args) > 1:
        generate(args[1], to_stdout=True)
        sys.exit(0)

    if args[0] == "--validate":
        registry = load_profiles()
        errors = validate_registry(registry)
        if errors:
            for e in errors:
                print(e)
            sys.exit(1)
        else:
            count = len(registry.get("profiles", []))
            print(f"[OK] Registry valid, {count} profiles checked")
        sys.exit(0)

    if args[0] == "--rollback":
        rollback()
        sys.exit(0)

    profile_name = args[0]
    to_stdout = "--stdout" in args
    generate(profile_name, to_stdout)
