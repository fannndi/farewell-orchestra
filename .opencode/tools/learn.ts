import { tool } from "@opencode-ai/plugin"
import * as fs from "fs"
import * as os from "os"
import * as path from "path"

// Lessons.md has multiple sections (lessons table → Sensor Coverage → Perf Log →
// Recurring Patterns). A naive appendFileSync at EOF would land new rows OUTSIDE the
// lessons table, so the insert position is bound to the MAIN lessons table (first
// `| date |` header → next `## ` section). Concurrent learn() calls are serialized
// with an exclusive lock: both queue up and persist (no lost rows). Lock lives in
// temp, not the vault.
const LOCK_RETRY_MS = 20
const LOCK_BUDGET_MS = 2000
const LOCK_STALE_MS = 3000

async function acquireLock(lockPath: string): Promise<boolean> {
  const deadline = Date.now() + LOCK_BUDGET_MS
  while (Date.now() < deadline) {
    try {
      const fd = fs.openSync(lockPath, "wx")
      fs.writeSync(fd, String(process.pid))
      fs.closeSync(fd)
      return true
    } catch {
      // Held by another call — steal if stale (crash leftover), else wait and retry
      try {
        if (Date.now() - fs.statSync(lockPath).mtimeMs > LOCK_STALE_MS) {
          fs.unlinkSync(lockPath)
          continue
        }
      } catch {
        // Lock vanished — retry immediately
      }
      await new Promise((r) => setTimeout(r, LOCK_RETRY_MS))
    }
  }
  return false
}

export default tool({
  description:
    "Log a lesson to Farewell-Knowlage/Lessons.md (Obsidian vault). Call this when orchestrator corrects an agent (non-trivial), when a pattern repeats 3x, or when a systemic fix is applied. Skip for typos/trivial.",
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
    const lessonsDir = path.join(path.dirname(worktree), "Farewell-Knowlage")
    const lessonsPath = path.join(lessonsDir, "Lessons.md")
    const date = new Date().toISOString().slice(0, 10)

    // Escape pipe characters for markdown table
    const esc = (s: string) => s.replace(/\|/g, "\\|").replace(/\r?\n/g, " ")
    const fixPart = args.verification
      ? `${esc(args.fix)} — verify:${args.verified} \`${esc(args.verification)}\``
      : esc(args.fix)
    const row = `| ${date} | ${esc(args.trigger)} | ${esc(args.error)} | ${esc(args.root_cause)} | ${fixPart} |\n`

    // Ensure target dir exists (first call fails without it)
    fs.mkdirSync(lessonsDir, { recursive: true })

    // Serialize concurrent learn() calls — read-modify-write without a lock drops
    // one row when two calls interleave. Lock lives in temp, not the vault.
    const lockPath = path.join(os.tmpdir(), "farewell-lessons.md.lock")
    const locked = await acquireLock(lockPath)

    try {
      // Read existing content (pure Node FS, no shell). Missing file → seed table header.
      let content: string
      if (fs.existsSync(lessonsPath)) {
        content = fs.readFileSync(lessonsPath, "utf-8")
      } else {
        content = "| Date | Trigger | Error | Root Cause | Fix |\n|---|---|---|---|---|\n"
      }

      const lines = content.split("\n")

      // Strict pipe detection: a real data row starts with | YYYY-MM-DD
      // This prevents false positives on header separator, unicode pipes, or unrelated markdown
      const DATA_ROW_RE = /^\|\s*\d{4}-\d{2}-\d{2}\s*\|/
      const SEPARATOR_RE = /^\|[-\s|]+\|?$/
      const TABLE_HEADER_RE = /^\|\s*date\s*\|/i

      // Bound the insert to the MAIN lessons table: from the first `| date |`
      // header row up to the next `## ` section. Later sections (Sensor Coverage,
      // Sub-Agent Performance Log) also contain date rows — scanning the whole file
      // would push new rows into those tables instead of the lessons table.
      let tableStart = -1
      let tableEnd = lines.length
      for (let i = 0; i < lines.length; i++) {
        if (tableStart === -1 && TABLE_HEADER_RE.test(lines[i])) {
          tableStart = i
        } else if (tableStart !== -1 && lines[i].startsWith("## ")) {
          tableEnd = i
          break
        }
      }
      if (tableStart === -1) {
        // No table header found — fall back to whole-file behavior
        tableStart = 0
      }

      let insertAt = -1

      // Strategy 1: find the last data row INSIDE the main table and insert after it
      for (let i = tableEnd - 1; i >= tableStart; i--) {
        if (DATA_ROW_RE.test(lines[i])) {
          insertAt = i + 1
          break
        }
      }

      // Strategy 2: no data rows yet — find the header separator and insert after it
      if (insertAt === -1) {
        for (let i = tableStart; i < tableEnd; i++) {
          if (SEPARATOR_RE.test(lines[i])) {
            insertAt = i + 1
            break
          }
        }
      }

      // Strategy 3: append at the end of the main table region (before trailing blanks)
      if (insertAt === -1) {
        // skip trailing empty lines inside the table region, then insert after
        let lastNonEmpty = tableEnd - 1
        while (lastNonEmpty >= tableStart && lines[lastNonEmpty].trim() === "") {
          lastNonEmpty--
        }
        insertAt = lastNonEmpty + 1
      }

      lines.splice(insertAt, 0, row)
      const newContent = lines.join("\n")

      try {
        fs.writeFileSync(lessonsPath, newContent, "utf-8")
      } catch (e: any) {
        return `## Learn Tool — ERROR\n\nCannot write Farewell-Knowlage/Lessons.md: ${e.message}`
      }
    } finally {
      if (locked) {
        try {
          fs.unlinkSync(lockPath)
        } catch {
          // best effort — lock will be stolen by the stale guard
        }
      }
    }

    return `Logged to Farewell-Knowlage/Lessons.md:\n  ${row.trim()}`
  },
})
