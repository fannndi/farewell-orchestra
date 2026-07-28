#!/bin/bash
BASE="$(dirname "$0")"
echo "=== Farewell Orchestra — Profile Switcher ==="
echo ""
echo " 1. V1 (Default) — deepseek-v4-flash + deepseek-free + north-mini-code  [WINNER]"
echo " 2. LIMITED — ollama/minimax-m3 + north-mini-code  [V1 base, flash replaced]"
echo ""
read -p "Choice (1-2): " CH
case "$CH" in
    1) SRC="$BASE/profiles/hybrid-v1.jsonc" ;;
    2) SRC="$BASE/profiles/opencode.limited.jsonc" ;;
    *) echo "Invalid choice." ; exit 1 ;;
esac
if [ ! -f "$SRC" ]; then echo "ERROR: File missing — $SRC"; exit 1; fi
cp "$SRC" "$BASE/opencode.jsonc" && echo "Copied to opencode.jsonc — Restart opencode to apply."
