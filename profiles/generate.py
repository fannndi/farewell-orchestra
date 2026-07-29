"""
Profile generator for opencode.jsonc
Usage:  python profiles/generate.py <profile-name> [--stdout]
          python profiles/generate.py default-oc
          python profiles/generate.py codex-or --stdout > opencode.jsonc

Reads profiles.json, generates full opencode.jsonc with correct model assignments.
"""

import json
import os
import sys

PROFILES_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_JSON = os.path.join(PROFILES_DIR, "profiles.json")
TEMP_FILE = os.path.join(PROFILES_DIR, "opencode.temp.jsonc")
ROOT_FILE = os.path.join(PROFILES_DIR, "..", "opencode.jsonc")

# ── boilerplate (shared across all profiles) ──────────────────────────

BOILERPLATE = {
    "$schema": "https://opencode.ai/config.json",
    "default_agent": "orchestrator",
    "instructions": ["AGENTS.md", ".opencode/agents/*.md"],
    "subagent_depth": 1,
    "share": "disabled",
    "permission": {
        "read": "allow", "edit": "allow", "glob": "allow", "grep": "allow",
        "list": "allow", "bash": "allow", "task": "allow", "webfetch": "allow",
        "websearch": "allow", "question": "allow", "todowrite": "allow",
        "lsp": "allow", "skill": "allow",
        "external_directory": {"*": "allow"}
    },
    "references": {
        "projects": {"path": "~/projects", "description": "Folder project Boss"},
        "opencode-sdk": {"repository": "anomalyco/opencode-sdk-js", "description": "OpenCode SDK"},
        "opencode-config": {"path": "~/.config/opencode", "description": "OpenCode global config", "hidden": True}
    },
    "autoupdate": "notify",
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
                "chunkTimeout": 120000
            }
        }
    },
    "experimental": {"primary_tools": ["todowrite", "question"]},
    "tool_output": {"max_lines": 2000, "max_bytes": 51200},
    "compaction": {
        "auto": True,
        "preserve_recent_tokens": 7000,
        "reserved": 25000,
        "prune": True
    },
    "watcher": {
        "ignore": [
            ".git/**", "node_modules/**", "dist/**", "build/**",
            ".next/**", ".venv/**", "venv/**",
            "__pycache__/**", ".pytest_cache/**"
        ]
    },
    "attachment": {
        "image": {
            "auto_resize": True,
            "max_width": 2000,
            "max_height": 2000,
            "max_base64_bytes": 5242880
        }
    },
    "lsp": True,
    "formatter": True
}

# Agent config template — only `model` changes per profile
AGENT_TEMPLATES = {
    "orchestrator": {
        "color": "#7c3aed",
        "description": "Workflow orchestrator",
        "mode": "primary",
        "request": {"body": {"temperature": 0.2}},
        "steps": 20,
        "prompt": "Decompose requests.",
        "permission": {
            "read": "allow", "edit": "allow", "glob": "allow", "grep": "allow",
            "list": "allow", "bash": "allow", "question": "allow", "skill": "allow",
            "todowrite": "allow", "lsp": "allow",
            "external_directory": {"*": "allow"},
            "task": {"*": "deny", "researcher": "allow", "reviewer": "allow", "executor": "allow"}
        }
    },
    "researcher": {
        "color": "#3b82f6",
        "description": "Read-only researcher",
        "mode": "subagent",
        "request": {"body": {"temperature": 0.1}},
        "steps": 18,
        "prompt": "Read-only. Return evidence with file:line.",
        "permission": {
            "read": "allow", "edit": "allow", "glob": "allow", "grep": "allow",
            "list": "allow", "bash": "allow", "webfetch": "allow", "websearch": "allow",
            "lsp": "allow", "skill": "allow",
            "external_directory": {"*": "allow"},
            "task": "deny"
        }
    },
    "reviewer": {
        "color": "#f59e0b",
        "description": "Read-only reviewer",
        "mode": "subagent",
        "request": {"body": {"temperature": 0.1}},
        "steps": 14,
        "prompt": "Read-only. Return prioritized findings.",
        "permission": {
            "read": "allow", "edit": "allow", "glob": "allow", "grep": "allow",
            "list": "allow", "bash": "allow", "webfetch": "allow", "websearch": "allow",
            "lsp": "allow", "skill": "allow",
            "external_directory": {"*": "allow"},
            "task": "deny"
        }
    },
    "executor": {
        "color": "#10b981",
        "description": "Implementation worker",
        "mode": "subagent",
        "request": {"body": {"temperature": 0.2}},
        "steps": 18,
        "prompt": "Implement only the scoped change.",
        "permission": {
            "read": "allow", "edit": "allow", "glob": "allow", "grep": "allow",
            "list": "allow", "bash": "allow", "lsp": "allow", "skill": "allow",
            "external_directory": {"*": "allow"},
            "task": "deny"
        }
    }
}

DISABLED_AGENTS = {
    "build": {"mode": "primary", "color": "primary", "disable": True},
    "plan": {"mode": "primary", "color": "secondary", "disable": True},
    "general": {
        "mode": "subagent", "disable": True,
        "permission": {"*": "deny", "read": "allow", "glob": "allow", "grep": "allow", "list": "allow", "task": "deny"}
    },
    "explore": {
        "mode": "subagent", "disable": True,
        "permission": {"*": "deny", "read": "allow", "glob": "allow", "grep": "allow", "list": "allow", "task": "deny"}
    }
}


def load_profiles():
    with open(PROFILES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def find_profile(registry, name):
    for p in registry["profiles"]:
        if p["name"] == name:
            return p
    return None


def collect_models(registry, profile):
    """Collect all unique model IDs used in this profile."""
    models = set()
    models.add(profile["model"])
    models.add(profile["small_model"])
    for agent_name, model_id in profile["agents"].items():
        models.add(model_id)
    return models


def build_agent_config(profile):
    """Build the agent section with correct models per profile."""
    agents = {}
    for name, template in AGENT_TEMPLATES.items():
        cfg = dict(template)
        cfg["model"] = profile["agents"].get(name, profile["model"])
        agents[name] = cfg

    # Hidden agents use small_model
    small = profile["small_model"]
    hidden = {
        "title": {"model": small, "mode": "primary", "hidden": True},
        "summary": {"model": small, "mode": "primary", "hidden": True},
        "compaction": {"model": small, "mode": "primary", "hidden": True, "steps": 8}
    }
    agents.update(hidden)
    agents.update(DISABLED_AGENTS)
    return agents


PROVIDER_PREFIX = "9router/"

def short_model_id(full_id):
    """Strip provider prefix for provider.models keys."""
    if full_id.startswith(PROVIDER_PREFIX):
        return full_id[len(PROVIDER_PREFIX):]
    return full_id


def build_provider_models(registry, profile):
    """Build provider.models section — only models used by this profile."""
    model_ids = collect_models(registry, profile)
    result = {}
    for mid in sorted(model_ids):
        cfg = registry["models"].get(mid, {"reasoning": True, "tool_call": True})
        key = short_model_id(mid)
        result[key] = {
            "name": key,
            "reasoning": cfg.get("reasoning", True),
            "tool_call": cfg.get("tool_call", True),
            "limit": cfg.get("limit", {"context": 128000, "output": 128000})
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
    config["model"] = profile["model"]
    config["small_model"] = profile["small_model"]
    config["provider"]["9router"]["models"] = build_provider_models(registry, profile)
    config["agent"] = build_agent_config(profile)

    output = json.dumps(config, indent=2, ensure_ascii=False)
    header = f"// Profile: {profile['label']}\n"

    if to_stdout:
        sys.stdout.write(header + output + "\n")
        return

    # Write to temp first, then atomically copy to root
    temp_path = os.path.abspath(TEMP_FILE)
    root_path = os.path.abspath(ROOT_FILE)

    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(header + output + "\n")
    print(f"[OK] Wrote temp: {temp_path}")

    # Validate JSON before replacing the real file
    try:
        with open(temp_path, "r", encoding="utf-8") as f:
            raw = f.read()
            json.loads(raw[raw.index("{"):])
    except Exception as e:
        print(f"[ERROR] Generated file invalid, NOT copying: {e}", file=sys.stderr)
        sys.exit(1)

    import shutil
    shutil.copy2(temp_path, root_path)
    print(f"[OK] Copied -> {root_path}  ({profile['label']})")


def short_model(mid):
    """Return short readable model name from full model ID."""
    s = short_model_id(mid)
    return s.replace("-ultra-550b-a55b", "").replace(":free", "")


def show_menu():
    """Interactive menu — pick a profile, generate."""
    registry = load_profiles()
    profiles = registry["profiles"]

    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 62)
        print("  SWITCH PROFILE — Farewell Orchestra")
        print("=" * 62)
        print(f"  {'#':<3} {'Profile':<14} {'Orch':<20} {'Res':<20} {'Rev/Exe':<20}")
        print("  " + "-" * 58)
        for i, p in enumerate(profiles, 1):
            orch = short_model(p["agents"].get("orchestrator", p["model"]))
            res = short_model(p["agents"].get("researcher", p["small_model"]))
            rev = short_model(p["agents"].get("reviewer", p["small_model"]))
            exe_note = "(same)" if p["agents"].get("reviewer") == p["agents"].get("executor") else ""
            print(f"  {i:<3} {p['name']:<14} {orch:<20} {res:<20} {rev:<20}")
        print("  " + "-" * 58)
        print(f"  0   Keluar")
        print()

        try:
            choice = input("  Pilihan [0-{}]: ".format(len(profiles))).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "0":
            print("\n  Bye.")
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(profiles):
                profile = profiles[idx]
                print(f"\n  >>> Memilih: {profile['name']} ({profile['label']})")
                generate(profile["name"])
                input("\n  [Enter] untuk kembali ke menu...")
            else:
                input(f"\n  Pilihan {choice} nggak ada. [Enter]...")
        except ValueError:
            input(f"\n  '{choice}' bukan angka. [Enter]...")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        registry = load_profiles()
        names = [p["name"] for p in registry["profiles"]]
        print("Usage:")
        print("  python profiles/generate.py <profile-name>   -> write temp -> copy to opencode.jsonc")
        print("  python profiles/generate.py --menu | -i      -> interactive menu")
        print("  python profiles/generate.py --stdout <name>  -> print to stdout")
        print(f"\nProfiles: {', '.join(names)}")
        sys.exit(0)

    if args[0] in ("--menu", "-i", "-m"):
        show_menu()
        sys.exit(0)

    if args[0] == "--stdout" and len(args) > 1:
        generate(args[1], to_stdout=True)
        sys.exit(0)

    profile_name = args[0]
    to_stdout = "--stdout" in args
    generate(profile_name, to_stdout)
