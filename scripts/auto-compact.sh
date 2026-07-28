#!/usr/bin/env bash
# auto-compact.sh — Check context usage, trigger compaction hint if >80% with loop guard

set -euo pipefail

# Loop guard: track last compaction turn
LAST_TURN_FILE="/tmp/opencode-compact-last-turn"
CURRENT_TURN="${OPENCODE_TURN:-0}"

# Heuristic: estimate context % from turn count (rough: ~1000 tokens/turn, 128k limit)
# If OPENCODE_CONTEXT_PCT env var exists, use it; else estimate
if [[ -n "${OPENCODE_CONTEXT_PCT:-}" ]]; then
    CONTEXT_PCT="$OPENCODE_CONTEXT_PCT"
else
    # Fallback: assume ~1000 tokens per turn, 128k limit = ~128 turns = 100%
    # So: context% = (current_turn / 128) * 100
    CONTEXT_PCT=$(( CURRENT_TURN * 100 / 128 ))
    [[ $CONTEXT_PCT -gt 100 ]] && CONTEXT_PCT=100
fi

# Read last compaction turn
LAST_TURN=0
if [[ -f "$LAST_TURN_FILE" ]]; then
    LAST_TURN=$(cat "$LAST_TURN_FILE" 2>/dev/null || echo 0)
fi

# Loop guard: don't nag if compacted within last 5 turns
TURN_DIFF=$(( CURRENT_TURN - LAST_TURN ))

echo "Context: ~${CONTEXT_PCT}% (turn $CURRENT_TURN, last compact at turn $LAST_TURN)"

if [[ $CONTEXT_PCT -gt 80 ]] && [[ $TURN_DIFF -gt 5 ]]; then
    echo "⚠️  Context >80%. Run \`/compact\` manually or wait for auto-compaction (enabled in config)."
    echo "$CURRENT_TURN" > "$LAST_TURN_FILE"
    exit 0
elif [[ $CONTEXT_PCT -gt 80 ]] && [[ $TURN_DIFF -le 5 ]]; then
    echo "⏳ Context >80% but compacted recently (turn $LAST_TURN). Waiting..."
    exit 0
else
    echo "✅ Context healthy (<80%)."
    exit 0
fi