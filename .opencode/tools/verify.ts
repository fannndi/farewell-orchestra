import { tool } from "@opencode-ai/plugin"
import { execSync } from "child_process"
import path from "path"

export default tool({
  description:
    "VERIFICATION GATE — Check agent output quality before proceeding to next orchestration stage. " +
    "Call this AFTER researcher/reviewer returns findings and BEFORE briefing executor. " +
    "If FAIL, reject output and ask agent to revise with specifics from check details. " +
    "If PASS, proceed to next stage. PARTIAL means warnings exist but can proceed cautiously.",
  args: {
    stage: tool.schema
      .enum(["research", "review", "implement"])
      .describe(
        "Pipeline stage: research (file refs + evidence), review (tags + BLOCKING), implement (files + JSON + git)"
      ),
    claims: tool.schema
      .string()
      .describe(
        "The agent output text to verify — paste the key findings/changes here"
      ),
    files: tool.schema
      .array(tool.schema.string())
      .optional()
      .default([])
      .describe("Files the agent claims to have read/written — for existence + syntax check"),
    spec: tool.schema
      .string()
      .optional()
      .default("")
      .describe("Original task spec from orchestrator — for scope creep detection"),
  },

  async execute(args, context) {
    const scriptPath = path.join(context.worktree, ".opencode/tools/verify.py")
    const input = JSON.stringify({
      stage: args.stage,
      claims: args.claims,
      files: args.files,
      spec: args.spec,
    })

    try {
      const raw = execSync(`python "${scriptPath}" "${input.replace(/"/g, '\\"')}"`, {
        encoding: "utf-8",
        timeout: 15000,
        env: { ...process.env, WORKTREE: context.worktree },
      })

      const result = JSON.parse(raw.trim())

      // Build human-readable output
      let output = `## Verification Gate — ${args.stage.toUpperCase()}\n\n`
      output += `**Result: ${result.summary}**\n\n`

      for (const check of result.checks) {
        const icon =
          check.status === "PASS" ? "  ✓" : check.status === "WARN" ? "  ⚠" : "  ✗"
        output += `${icon} ${check.name}: ${check.detail}\n`
      }

      output += `\n${result.passed}/${result.total} checks passed`
      if (result.warnings > 0) output += `, ${result.warnings} warnings`
      if (result.failed > 0) output += `, ${result.failed} FAILED`

      if (!result.pass) {
        output +=
          "\n\n⛔ VERIFICATION FAILED. Do NOT proceed. Send this report back to the agent with: 'Fix the FAIL items above and resubmit.'"
      } else if (result.warnings > 0) {
        output +=
          "\n\n⚠ PASSED with warnings. Can proceed but note warnings."
      } else {
        output += "\n\n✅ All clean. Proceed to next stage."
      }

      return output
    } catch (e: any) {
      return `## Verification Gate — ERROR\n\nTool failed: ${e.message}\n\nVerify manually.`
    }
  },
})
