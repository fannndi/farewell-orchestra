import { tool } from "@opencode-ai/plugin"
import { execFileSync, spawnSync } from "child_process"

// Python-first: 'python' terbukti respond; 'python3' di Windows sering WindowsApps
// stub yang hang atau return garbage. Probe via spawnSync + timeout pendek (2000ms)
// + status check, supaya stub terdeteksi cepat (ETIMEDOUT / non-zero) dan fallback
// graceful ke 'python' — bukan hang di module load.
function detectPython(): string {
  for (const cmd of ["python", "python3"]) {
    try {
      const probe = spawnSync(cmd, ["--version"], {
        timeout: 2000,
        stdio: "pipe",
        encoding: "utf-8",
      })
      if (probe.status === 0) return cmd
    } catch {
      // hang/timeout atau spawn error — lanjut ke command berikutnya
    }
  }
  return "python" // graceful fallback; callers handle failure
}
const pythonCmd = detectPython()
import * as fs from "fs"
import * as path from "path"

export default tool({
  description:
    "Check harness health: validate profiles.json, show active profile. " +
    "Call this when boss asks /check, or when orchestrator needs health info before dispatching. " +
    "Use format:'json' for machine-readable output.",
  args: {
    check: tool.schema
      .enum(["all", "profiles", "active"])
      .optional()
      .default("all")
      .describe("What to check: all (default), profiles, or active profile"),
    format: tool.schema
      .enum(["text", "json"])
      .optional()
      .default("text")
      .describe("Output format: text (human) or json (machine, matches check.md schema)"),
  },

  async execute(args, context) {
    const worktree = path.isAbsolute(context.worktree) ? context.worktree : path.resolve(process.cwd(), context.worktree)
    const results: string[] = []
    const errors: string[] = []

    // Build a JSON payload for format:json
    const jsonPayload: any = {
      timestamp: new Date().toISOString(),
      active_project: path.basename(worktree),
    }

    // 1. Active profile — pure Node.js, no shell
    const configPath = path.join(worktree, "opencode.jsonc")
    let activeModel = "?"
    let smallModel = "?"
    let agentModels: Record<string, string> = {}
    let agentSteps: Record<string, number> = {}
    try {
      const raw = fs.readFileSync(configPath, "utf-8")
      const jsonStart = raw.indexOf("{")
      if (jsonStart >= 0) {
        const config = JSON.parse(raw.slice(jsonStart))
        activeModel = config.model || "?"
        smallModel = config.small_model || "?"
        results.push(`Active model: ${activeModel}`)
        results.push(`Small model:  ${smallModel}`)

        // Extract agent info
        if (config.agent) {
          for (const [name, agent] of Object.entries(config.agent) as any) {
            if (agent.model) agentModels[name] = agent.model
            if (agent.steps) agentSteps[name] = agent.steps
          }
        }
      }
    } catch {
      errors.push("Cannot read opencode.jsonc")
    }

    // 2. Profile validation — execFileSync is safe because generate.py is a known script
    let profilesValid = false
    let profilesTotal = 0
    if (args.check === "all" || args.check === "profiles") {
      try {
        const valOut = execFileSync(pythonCmd, ['profiles/generate.py', '--validate'], {
          cwd: worktree,
          encoding: "utf-8",
          timeout: 10000,
          shell: false,
        })
        profilesValid = true
        results.push(`Validation: ${valOut.trim()}`)
      } catch (e: any) {
        errors.push(`Validation failed: ${e.message}`)
      }
    }

    // 3. Active profile detail — pure Node.js
    let availableProfiles: string[] = []
    if (args.check === "all" || args.check === "active") {
      try {
        const profilesRaw = fs.readFileSync(path.join(worktree, "profiles/profiles.json"), "utf-8")
        const profilesData = JSON.parse(profilesRaw)
        availableProfiles = profilesData.profiles.map((p: any) => p.name)
        profilesTotal = availableProfiles.length
        results.push(`Available profiles (${profilesTotal}): ${availableProfiles.join(", ")}`)
      } catch {
        errors.push("Cannot list profiles")
      }
    }

    // --- JSON output ---
    if (args.format === "json") {
      jsonPayload.profile = activeModel
      jsonPayload.small_model = smallModel

      // Agents info
      const agents: Record<string, any> = {}
      for (const name of ["orchestrator", "researcher", "reviewer", "executor"]) {
        if (agentModels[name]) {
          agents[name] = {
            model: agentModels[name],
            steps_limit: agentSteps[name] || 0,
          }
        }
      }
      jsonPayload.agents = agents
      jsonPayload.profiles = {
        total: profilesTotal,
        valid: profilesValid,
        names: availableProfiles,
      }
      jsonPayload.errors = errors.length > 0 ? errors : undefined
      jsonPayload.healthy = errors.length === 0

      return JSON.stringify(jsonPayload, null, 2)
    }

    // --- Text output (default) ---
    let output = "## Harness Status\n\n"
    if (results.length > 0) {
      output += results.map((r) => `  ✓ ${r}`).join("\n") + "\n"
    }
    if (errors.length > 0) {
      output += "\n" + errors.map((e) => `  ✗ ${e}`).join("\n") + "\n"
    }
    if (errors.length === 0) {
      output += "\n  ✓ All checks passed"
    }

    return output
  },
})
