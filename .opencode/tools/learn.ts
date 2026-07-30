import { tool } from "@opencode-ai/plugin"
import * as fs from "fs"
import * as path from "path"

export default tool({
  description:
    "Log a lesson to LESSONS.md. Call this when orchestrator corrects an agent (non-trivial), when a pattern repeats 3x, or when a systemic fix is applied. Skip for typos/trivial.",
  args: {
    trigger: tool.schema.string().describe("What triggered this? e.g. 'executor failed 2x on --diff'"),
    error: tool.schema.string().describe("What error/bug happened?"),
    root_cause: tool.schema.string().describe("Why did it happen?"),
    fix: tool.schema.string().describe("What was the fix/changed?"),
    verification: tool.schema.string().optional().describe("Command used to verify the fix, e.g. 'python generate.py --validate'"),
    verified: tool.schema.enum(["pass", "fail", "unverified"]).optional().default("unverified").describe("Did the verification pass?"),
  },

  async execute(args, context) {
    const worktree = context.worktree
    const lessonsPath = path.join(worktree, "LESSONS.md")
    const date = new Date().toISOString().slice(0, 10)

    // Escape pipe characters for markdown table
    const esc = (s: string) => s.replace(/\|/g, "\\|")
    const fixPart = args.verification
      ? `${esc(args.fix)} — verify:${args.verified} \`${esc(args.verification)}\``
      : esc(args.fix)
    const row = `| ${date} | ${esc(args.trigger)} | ${esc(args.error)} | ${esc(args.root_cause)} | ${fixPart} |\n`

    // Read existing content (pure Node FS, no shell)
    let content: string
    try {
      content = fs.readFileSync(lessonsPath, "utf-8")
    } catch (e: any) {
      return `## Learn Tool — ERROR\n\nCannot read LESSONS.md: ${e.message}\n\nPath: ${lessonsPath}`
    }

    const lines = content.split("\n")

    // Strict pipe detection: a real data row starts with | YYYY-MM-DD
    // This prevents false positives on header separator, unicode pipes, or unrelated markdown
    const DATA_ROW_RE = /^\|\s*\d{4}-\d{2}-\d{2}\s*\|/
    const SEPARATOR_RE = /^\|[-\s|]+\|?$/

    let insertAt = -1

    // Strategy 1: find the last existing data row and insert after it
    for (let i = lines.length - 1; i >= 0; i--) {
      if (DATA_ROW_RE.test(lines[i])) {
        insertAt = i + 1
        break
      }
    }

    // Strategy 2: no data rows yet — find the header separator and insert after it
    if (insertAt === -1) {
      for (let i = 0; i < lines.length; i++) {
        if (SEPARATOR_RE.test(lines[i])) {
          insertAt = i + 1
          break
        }
      }
    }

    // Strategy 3: append before trailing blank line
    if (insertAt === -1) {
      // skip trailing empty lines, then insert after
      let lastNonEmpty = lines.length - 1
      while (lastNonEmpty >= 0 && lines[lastNonEmpty].trim() === "") {
        lastNonEmpty--
      }
      insertAt = lastNonEmpty + 1
    }

    lines.splice(insertAt, 0, row)
    const newContent = lines.join("\n")

    try {
      fs.writeFileSync(lessonsPath, newContent, "utf-8")
    } catch (e: any) {
      return `## Learn Tool — ERROR\n\nCannot write LESSONS.md: ${e.message}`
    }

    return `Logged to LESSONS.md:\n  ${row.trim()}`
  },
})
