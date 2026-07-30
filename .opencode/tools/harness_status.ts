import { tool } from "@opencode-ai/plugin"
import { execFileSync } from "child_process"
import * as fs from "fs"
import * as path from "path"

export default tool({
  description:
    "Check harness health: validate profiles.json, show active profile, sensor coverage status. Call this when boss asks /check, /status, or when orchestrator needs health info before dispatching.",
  args: {
    check: tool.schema
      .enum(["all", "profiles", "sensors", "active"])
      .optional()
      .default("all")
      .describe("What to check: all (default), profiles, sensors, or active profile"),
  },

  async execute(args, context) {
    const worktree = context.worktree
    const results: string[] = []
    const errors: string[] = []

    // 1. Active profile — pure Node.js, no shell
    const configPath = path.join(worktree, "opencode.jsonc")
    try {
      const raw = fs.readFileSync(configPath, "utf-8")
      const jsonStart = raw.indexOf("{")
      if (jsonStart >= 0) {
        const config = JSON.parse(raw.slice(jsonStart))
        results.push(`Active model: ${config.model || "?"}`)
        results.push(`Small model:  ${config.small_model || "?"}`)
      }
    } catch {
      errors.push("Cannot read opencode.jsonc")
    }

    // 2. Profile validation — execFileSync is safe because generate.py is a known script
    if (args.check === "all" || args.check === "profiles") {
      try {
        const valOut = execFileSync('python', ['profiles/generate.py', '--validate'], {
          cwd: worktree,
          encoding: "utf-8",
          timeout: 10000,
          shell: false,
        })
        results.push(`Validation: ${valOut.trim()}`)
      } catch (e: any) {
        errors.push(`Validation failed: ${e.message}`)
      }
    }

    // 3. Active profile detail — pure Node.js
    if (args.check === "all" || args.check === "active") {
      try {
        const profilesRaw = fs.readFileSync(path.join(worktree, "profiles/profiles.json"), "utf-8")
        const profilesData = JSON.parse(profilesRaw)
        const profileNames = profilesData.profiles.map((p: any) => p.name)
        results.push(`Available profiles (${profileNames.length}): ${profileNames.join(", ")}`)
      } catch {
        errors.push("Cannot list profiles")
      }
    }

    // 4. Sensor coverage (from LESSONS.md) — pure Node.js
    if (args.check === "all" || args.check === "sensors") {
      try {
        const lessonsPath = path.join(worktree, "LESSONS.md")
        const lessonsContent = fs.readFileSync(lessonsPath, "utf-8")
        const sensorSection = lessonsContent.match(/## Sensor Coverage[\s\S]*?(?=## |$)/)
        if (sensorSection) {
          const section = sensorSection[0]
          const oks = (section.match(/✅/g) || []).length
          const nos = (section.match(/❌/g) || []).length
          const partials = (section.match(/⚠️/g) || []).length
          results.push(`Sensor coverage: ${oks} OK, ${nos} MISSING, ${partials} PARTIAL`)
        } else {
          errors.push("Sensor coverage section not found in LESSONS.md")
        }
      } catch {
        errors.push("Cannot read sensor coverage")
      }
    }

    // Build report
    let output = "## Harness Status\n\n"
    if (results.length > 0) {
      output += results.map((r) => `  ✓ ${r}`).join("\n") + "\n"
    }
    if (errors.length > 0) {
      output += "\n" + errors.map((e) => `  ✗ ${e}`).join("\n") + "\n"
    }
    if (errors.length === 0 && args.check !== "sensors") {
      output += "\n  ✓ All checks passed"
    }

    return output
  },
})
