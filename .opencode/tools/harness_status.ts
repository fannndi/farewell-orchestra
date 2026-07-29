import { tool } from "@opencode-ai/plugin"
import { execSync } from "child_process"
import path from "path"

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

    // 1. Active profile
    const opencodeConfig = path.join(worktree, "opencode.jsonc")
    try {
      const raw = execSync(`python -c "import json; c=open('${opencodeConfig}','r',encoding='utf-8').read(); d=json.loads(c[c.index('{'):]); print(d.get('model','?')); print(d.get('small_model','?'))"`, {
        encoding: "utf-8",
        timeout: 5000,
      })
        .trim()
        .split("\n")
      results.push(`Active model: ${raw[0]}`)
      results.push(`Small model:  ${raw[1]}`)
    } catch {
      errors.push("Cannot read opencode.jsonc")
    }

    // 2. Profile validation
    if (args.check === "all" || args.check === "profiles") {
      try {
        const valOut = execSync(`python profiles/generate.py --validate`, {
          cwd: worktree,
          encoding: "utf-8",
          timeout: 10000,
        })
        results.push(`Validation: ${valOut.trim()}`)
      } catch (e: any) {
        errors.push(`Validation failed: ${e.message}`)
      }
    }

    // 3. Active profile detail
    if (args.check === "all" || args.check === "active") {
      try {
        const allProfiles = execSync(
          `python -c "import json; f=open('profiles/profiles.json','r',encoding='utf-8'); d=json.load(f); [print(p['name']) for p in d['profiles']]"`,
          { cwd: worktree, encoding: "utf-8", timeout: 5000 }
        )
          .trim()
          .split("\n")
        results.push(`Available profiles (${allProfiles.length}): ${allProfiles.join(", ")}`)
      } catch {
        errors.push("Cannot list profiles")
      }
    }

    // 4. Sensor coverage (from LESSONS.md)
    if (args.check === "all" || args.check === "sensors") {
      try {
        const sensors = execSync(
          `python -c "
import re
c=open('LESSONS.md','r',encoding='utf-8').read()
section=c[c.index('## Sensor Coverage'):c.index('## ',(c.index('## Sensor Coverage')+20))] if '## Sensor Coverage' in c else ''
oks=section.count(chr(10004))
nos=section.count('❌')
partials=section.count('⚠️')
print(f'Sensor coverage: {oks} OK, {nos} MISSING, {partials} PARTIAL')
"`,
          { cwd: worktree, encoding: "utf-8", timeout: 5000 }
        )
        results.push(sensors.trim())
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
