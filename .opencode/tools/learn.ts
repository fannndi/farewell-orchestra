import { tool } from "@opencode-ai/plugin"
import { execSync } from "child_process"
import path from "path"

export default tool({
  description:
    "Log a lesson to LESSONS.md. Call this when orchestrator corrects an agent (non-trivial), when a pattern repeats 3x, or when a systemic fix is applied. Skip for typos/trivial.",
  args: {
    trigger: tool.schema.string().describe("What triggered this? e.g. 'executor failed 2x on --diff'"),
    error: tool.schema.string().describe("What error/bug happened?"),
    root_cause: tool.schema.string().describe("Why did it happen?"),
    fix: tool.schema.string().describe("What was the fix/changed?"),
  },

  async execute(args, context) {
    const worktree = context.worktree
    const lessonsPath = path.join(worktree, "LESSONS.md")
    const date = new Date().toISOString().slice(0, 10)

    // Escape pipe characters for markdown table
    const esc = (s: string) => s.replace(/\|/g, "\\|")
    const row = `| ${date} | ${esc(args.trigger)} | ${esc(args.error)} | ${esc(args.root_cause)} | ${esc(args.fix)} |\n`

    // Find the end of the existing table (after the last data row)
    const content = execSync(`type "${lessonsPath}"`, { encoding: "utf-8", timeout: 5000 })

    // Find where to insert: after the separator line (|---|) and any existing data rows
    const lines = content.split("\n")
    let insertAt = -1
    for (let i = lines.length - 1; i >= 0; i--) {
      if (lines[i].startsWith("|") && lines[i].includes("|") && !lines[i].includes("---")) {
        insertAt = i + 1
        break
      }
    }
    if (insertAt === -1) {
      // fallback: find the table header separator
      for (let i = 0; i < lines.length; i++) {
        if (lines[i].includes("|---")) {
          insertAt = i + 2 // after separator + first data row
          break
        }
      }
    }
    if (insertAt === -1) insertAt = lines.length - 1

    lines.splice(insertAt, 0, row)
    const newContent = lines.join("\n")

    execSync(
      `set-content -Path "${lessonsPath}" -Value @"
${newContent}
"@ -Encoding utf8`,
      { encoding: "utf-8", timeout: 5000, shell: "powershell" }
    )

    return `Logged to LESSONS.md:\n  | ${date} | ${args.trigger} | ${args.error} | ${args.root_cause} | ${args.fix} |`
  },
})
