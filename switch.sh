#!/bin/bash
echo "========================================"
echo "  Farewell Orchestra — Profile Switcher"
echo "========================================"
echo ""
echo "Pilih profile:"
echo "  1. Paid       (DeepSeek V4 Pro + Flash)"
echo "  2. Hybrid     (DeepSeek Flash + free)"
echo "  3. Free       (Nemotron + North Mini)"
echo ""
read -p "Pilihan (1-3): " choice

case "$choice" in
  1) cp profiles/opencode.paid.jsonc opencode.jsonc
     echo "[OK] Profile: Paid" ;;
  2) cp profiles/opencode.hybrid.jsonc opencode.jsonc
     echo "[OK] Profile: Hybrid" ;;
  3) cp profiles/opencode.free.jsonc opencode.jsonc
     echo "[OK] Profile: Free" ;;
  *) echo "[ERROR] Pilihan tidak valid." ;;
esac
