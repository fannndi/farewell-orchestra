#!/bin/bash
BASE="$(dirname "$0")"
echo "========================================"
echo "  Farewell Orchestra — Profile Switcher"
echo "========================================"
echo ""
echo "Pilih profile:"
echo "  1. Paid       (DeepSeek V4 Pro + Flash)"
echo "  2. Hybrid     (2 paid + 2 free)"
echo "  3. Free       (Nemotron + North Mini)"
echo ""
read -rp "Pilihan (1-3): " choice

case "$choice" in
  1)
    cp "$BASE/profiles/opencode.paid.jsonc" "$BASE/opencode.jsonc"
    echo "[OK] Profile: Paid" ;;
  2)
    cp "$BASE/profiles/opencode.hybrid.jsonc" "$BASE/opencode.jsonc"
    echo "[OK] Profile: Hybrid" ;;
  3)
    cp "$BASE/profiles/opencode.free.jsonc" "$BASE/opencode.jsonc"
    echo "[OK] Profile: Free" ;;
  *)
    echo "[ERROR] Pilihan tidak valid: '$choice'. Masukkan 1, 2, atau 3."
    exit 1 ;;
esac

if [ ! -f "$BASE/opencode.jsonc" ]; then
  echo "[ERROR] opencode.jsonc tidak ditemukan setelah switch."
  exit 1
fi
echo "[DONE] Config aktif: $(basename "$BASE/opencode.jsonc")"