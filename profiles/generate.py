"""
Profile generator for opencode.jsonc
Usage:
  python profiles/generate.py <profile-name>         Generate & copy to opencode.jsonc
  python profiles/generate.py --stdout <name>        Print to stdout
  python profiles/generate.py --validate             Check profiles.json integrity
"""

import json, os, sys, time, shutil, glob as glob_mod, io

# Fix Windows stdout encoding for Unicode
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

PROFILES_DIR = os.path.dirname(os.path.abspath(__file__))
PROFILES_JSON = os.path.join(PROFILES_DIR, "profiles.json")
TEMP_FILE = os.path.join(PROFILES_DIR, "opencode.temp.jsonc")
ROOT_FILE = os.path.join(PROFILES_DIR, "..", "opencode.jsonc")
BACKUP_DIR = os.path.join(PROFILES_DIR, "backups")
MAX_BACKUPS = 3
PROVIDER_PREFIX = "9router/"

# ── Agent templates ──────────────────────────────────────────────────
# Only `model` changes per profile. Rules are in AGENTS.md + skills.

AGENT_TEMPLATES = {
    "orchestrator": {
        "color": "#7c3aed",
        "description": "Workflow orchestrator",
        "mode": "primary",
        "request": {"body": {"temperature": 0.2}},
        "steps": 300,
        "prompt": "Orchestrator: prepare → decompose → fan-out parallel via `task` tool → synthesize → brief executor. Load skill: prepare + orchestrate. JANGAN nulis kode. Baca .opencode/tools/persona-context-orchestrator.md untuk persona lengkap.",
        "permission": {
            "read": {"*.md": "allow", "*": "ask"},
            "edit": {"sub-project.md": "allow", "*.md": "deny", "*": "deny"},
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
        "steps": 200,
        "prompt": "Read-only investigator. Return evidence file:line. Load skill: research. Baca .opencode/tools/persona-context-researcher.md untuk persona lengkap.",
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
        "steps": 200,
        "prompt": "Read-only auditor. STRIDE analysis. Return [TAG] file:line. Load skill: review. Baca .opencode/tools/persona-context-reviewer.md untuk persona lengkap.",
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
        "steps": 300,
        "prompt": "Implement per brief. YAGNI. Verify before report. Load skill: implement. Baca .opencode/tools/persona-context-executor.md untuk persona lengkap.",
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

HIDDEN_AGENTS = ["title", "summary", "compaction"]


def load_profiles():
    try:
        with open(PROFILES_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


def find_profile(registry, name):
    return next((p for p in registry["profiles"] if p["name"] == name), None)


def build_agent_config(profile):
    agents = {}
    for name, template in AGENT_TEMPLATES.items():
        cfg = dict(template)
        agent_data = profile["agents"].get(name)
        cfg["model"] = (
            agent_data["model"] if isinstance(agent_data, dict) else agent_data
        )
        agents[name] = cfg

    # Hidden agents use orchestrator model
    orch = profile["agents"].get("orchestrator", {})
    model = orch["model"] if isinstance(orch, dict) else orch
    for name in HIDDEN_AGENTS:
        agents[name] = {
            "model": model,
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
        }
    if "compaction" in agents:
        agents["compaction"]["steps"] = 8

    agents.update(DISABLED_AGENTS)
    return agents


def build_provider_models(registry, profile):
    models = set()
    for agent_data in profile.get("agents", {}).values():
        if isinstance(agent_data, dict):
            models.add(agent_data.get("model", ""))
            models.add(agent_data.get("small_model", ""))
        else:
            models.add(agent_data)
    models.discard("")

    result = {}
    for mid in sorted(models):
        cfg = registry["models"].get(mid, {"reasoning": True, "tool_call": True})
        key = mid[len(PROVIDER_PREFIX) :] if mid.startswith(PROVIDER_PREFIX) else mid
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
        print(
            f"[ERROR] Profile '{profile_name}' not found. Available: {', '.join(names)}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Build config
    orch = profile["agents"].get("orchestrator", {})
    model = orch["model"] if isinstance(orch, dict) else orch
    small_model = profile.get("small_model", model)

    config = {
        "$schema": "https://opencode.ai/config.json",
        "default_agent": "orchestrator",
        "instructions": ["AGENTS.md", "cross-project/guide.md", ".opencode/soul.md"],
        "subagent_depth": 2,
        "share": "disabled",
        "shell": "pwsh",
        "snapshot": True,
        "enabled_providers": ["9router"],
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
                "prepare": "allow",
                "orchestrate": "allow",
                "research": "allow",
                "review": "allow",
                "implement": "allow",
                "bootstrap-project": "allow",
                "kiss-checklist": "allow",
                "anti-patterns": "allow",
                "simplification": "allow",
                "complexity-budget": "allow",
                "progress-tracker": "allow",
                "error-handler": "allow",
                "context-manager": "allow",
                "tdd": "allow",
                "code-review": "allow",
                "diagnose-bugs": "allow",
                "handoff": "allow",
                "domain-modeling": "allow",
                "session-state": "allow",
                "task-decomposer": "allow",
                "agent-protocol": "allow",
                "feedback-loop": "allow",
                "context-window": "allow",
                "task-priority": "allow",
                "quality-gates": "allow",
                "agent-monitor": "allow",
                "kiss-automation": "allow",
                "edge-cases": "allow",
            },
        },
        "references": {
            "projects": {"path": "~/projects", "description": "Folder project"},
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
                "models": build_provider_models(registry, profile),
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
        "lsp": {
            "typescript": {
                "command": "typescript-language-server",
                "args": ["--stdio"],
            },
        },
        "formatter": {
            "default": "prettier",
            "languages": {
                "typescript": "prettier",
                "javascript": "prettier",
                "json": "prettier",
                "markdown": "prettier",
                "python": "black",
            },
        },
        "model": model,
        "small_model": small_model,
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
        "agent": build_agent_config(profile),
    }

    output = json.dumps(config, indent=2, ensure_ascii=False)
    header = f"// Profile: {profile['label']}\n"

    if to_stdout:
        sys.stdout.write(header + output + "\n")
        return

    # No-op detection
    root_path = os.path.abspath(ROOT_FILE)
    if os.path.isfile(root_path):
        try:
            with open(root_path, "r", encoding="utf-8") as f:
                existing = f.read()
            if existing[existing.index("{") :].strip() == output.strip():
                print(f"[OK] Already active: {profile['label']}")
                return
        except Exception:
            pass

    # Write temp, validate, copy
    temp_path = os.path.abspath(TEMP_FILE)
    with open(temp_path, "w", encoding="utf-8") as f:
        f.write(header + output + "\n")

    try:
        with open(temp_path, "r", encoding="utf-8") as f:
            raw = f.read()
        json.loads(raw[raw.index("{") :])
    except Exception as e:
        print(f"[ERROR] Invalid JSON, NOT copying: {e}", file=sys.stderr)
        sys.exit(1)

    # Backup existing
    if os.path.isfile(root_path):
        try:
            os.makedirs(BACKUP_DIR, exist_ok=True)
            ts = time.strftime("%Y%m%d-%H%M%S")
            shutil.copy2(root_path, os.path.join(BACKUP_DIR, f"opencode.{ts}.jsonc"))
            backups = sorted(
                glob_mod.glob(os.path.join(BACKUP_DIR, "opencode.*.jsonc"))
            )
            while len(backups) > MAX_BACKUPS:
                os.remove(backups.pop(0))
        except Exception as e:
            print(f"[WARN] Backup failed: {e}", file=sys.stderr)

    shutil.copy2(temp_path, root_path)
    print(f"[OK] {root_path} ({profile['label']})")


def validate_registry(registry):
    errors = []
    seen = set()
    for p in registry.get("profiles", []):
        name = p.get("name", "?")
        if name in seen:
            errors.append(f"[ERROR] Duplicate: '{name}'")
        seen.add(name)
        for field in ("name", "label"):
            if field not in p:
                errors.append(f"[ERROR] '{name}' missing '{field}'")
    if not registry.get("profiles"):
        errors.append("[WARN] No profiles")
    return errors


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        registry = load_profiles()
        names = [p["name"] for p in registry["profiles"]]
        print(
            f"Usage:\n  python profiles/generate.py <name>\n  python profiles/generate.py --stdout <name>\n  python profiles/generate.py --validate\n\nProfiles: {', '.join(names)}"
        )
        sys.exit(0)

    if args[0] == "--stdout" and len(args) > 1:
        generate(args[1], to_stdout=True)
    elif args[0] == "--validate":
        registry = load_profiles()
        errors = validate_registry(registry)
        if errors:
            for e in errors:
                print(e)
            sys.exit(1)
        print(f"[OK] Valid, {len(registry['profiles'])} profiles")
    else:
        generate(args[0])
