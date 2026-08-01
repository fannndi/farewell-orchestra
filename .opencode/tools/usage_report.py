#!/usr/bin/env python3
"""Usage report: request count per role + cost/tokens dari opencode.db (read-only).

Output bilingual EN-ID, gaya Farewell Orchestra. Dipanggil orchestrator
di root farewell-orchestra: python .opencode/tools/usage_report.py
"""
import argparse
import json
import os
import sqlite3
import sys
import time

ROLES = ["orchestrator", "reviewer", "researcher", "executor"]
DAY_MS = 86400 * 1000


def find_db():
    """Cari opencode.db — default ~/.local/share/opencode, fallback %LOCALAPPDATA%\\opencode."""
    candidates = [
        os.path.expanduser("~/.local/share/opencode/opencode.db"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "opencode", "opencode.db"),
    ]
    for p in candidates:
        if p and os.path.isfile(p):
            return p
    return None


def connect(db_path):
    # mode=ro: read-only, tidak pernah nulis ke DB
    return sqlite3.connect("file:" + db_path.replace("\\", "/") + "?mode=ro", uri=True)


def main():
    ap = argparse.ArgumentParser(description="Usage report per role dari opencode.db (read-only)")
    ap.add_argument("--today", action="store_true", help="hanya request di 24 jam terakhir")
    ap.add_argument("--project", metavar="NAME", help="filter session/project (project_id atau directory LIKE)")
    ap.add_argument("--json", action="store_true", help="output JSON untuk parsing")
    args = ap.parse_args()

    db_path = find_db()
    if not db_path:
        msg = (
            "Error: opencode.db tidak ditemukan.\n"
            "Dicari di: ~/.local/share/opencode/opencode.db dan %LOCALAPPDATA%\\opencode\\opencode.db\n"
            "Jalankan opencode dulu supaya DB ke-create, atau cek lokasi DB via Get-ChildItem."
        )
        print(msg, file=sys.stderr)
        sys.exit(1)

    now_ms = int(time.time() * 1000)
    since_ms = now_ms - DAY_MS
    filters = {"today": args.today, "project": args.project}

    try:
        conn = connect(db_path)
        cur = conn.cursor()

        # --- request count per role dari message.data.agent ---
        msg_where, msg_params = [], []
        if args.project:
            msg_where.append(
                "session_id IN (SELECT id FROM session WHERE directory LIKE ? OR project_id LIKE ?)"
            )
            msg_params += [f"%{args.project}%"] * 2
        if args.today:
            msg_where.append("time_created >= ?")
            msg_params.append(since_ms)
        msg_sql = "SELECT json_extract(data, '$.agent') AS agent, COUNT(*) FROM message"
        if msg_where:
            msg_sql += " WHERE " + " AND ".join(msg_where)
        msg_sql += " GROUP BY agent"

        counts = {r: 0 for r in ROLES + ["other"]}
        for agent, cnt in cur.execute(msg_sql, msg_params).fetchall():
            if agent is None:
                continue  # data JSON null / tanpa field agent -> skip
            key = agent if agent in ROLES else "other"
            counts[key] += cnt

        # --- cost + tokens dari session GROUP BY agent ---
        ses_where, ses_params = [], []
        if args.project:
            ses_where.append("(directory LIKE ? OR project_id LIKE ?)")
            ses_params += [f"%{args.project}%"] * 2
        if args.today:
            ses_where.append("time_created >= ?")
            ses_params.append(since_ms)
        ses_sql = "SELECT agent, SUM(cost), SUM(tokens_input), SUM(tokens_output) FROM session"
        if ses_where:
            ses_sql += " WHERE " + " AND ".join(ses_where)
        ses_sql += " GROUP BY agent"

        costs = {r: [0.0, 0, 0] for r in ROLES + ["other"]}  # [cost, tokens_in, tokens_out]
        for agent, cost, tin, tout in cur.execute(ses_sql, ses_params).fetchall():
            key = agent if (agent and agent in ROLES) else "other"
            costs[key][0] += cost or 0.0
            costs[key][1] += tin or 0
            costs[key][2] += tout or 0

        conn.close()
    except sqlite3.OperationalError as e:
        if "no such table" in str(e):
            print(
                "Error: tabel belum ada (migration opencode belum jalan).\n"
                "Jalankan opencode dulu supaya tabel message/session ke-create.",
                file=sys.stderr,
            )
        else:
            print(f"Error: gagal query opencode.db: {e}", file=sys.stderr)
        sys.exit(1)

    total = [sum(v[0] for v in costs.values()), sum(v[1] for v in costs.values()), sum(v[2] for v in costs.values())]
    total_req = sum(counts.values())

    def fmt_cost(c):
        return f"${c:.2f}"

    def fmt_tok(tin, tout):
        return f"{tin // 1000}k / {tout // 1000}k"

    if args.json:
        print(json.dumps({
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "filters": filters,
            "roles": [
                {"role": r, "requests": counts[r], "cost": round(costs[r][0], 4),
                 "tokens_input": costs[r][1], "tokens_output": costs[r][2]}
                for r in ROLES + ["other"]
            ],
            "total": {"requests": total_req, "cost": round(total[0], 4),
                      "tokens_input": total[1], "tokens_output": total[2]},
        }, indent=2))
        return

    print("## Usage Report")
    print("| Role | Requests | Cost | Tokens in/out |")
    print("|------|----------|------|---------------|")
    for r in ROLES + ["other"]:
        print(f"| {r} | {counts[r]} | {fmt_cost(costs[r][0])} | {fmt_tok(costs[r][1], costs[r][2])} |")
    print(f"| **TOTAL** | **{total_req}** | **{fmt_cost(total[0])}** | **{fmt_tok(total[1], total[2])}** |")


if __name__ == "__main__":
    main()
