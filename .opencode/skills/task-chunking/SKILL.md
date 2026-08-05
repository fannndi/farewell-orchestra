---
name: task-chunking
description: Use when a task spans 3+ questions, 3+ files, or 2+ output formats, OR when a sub-agent returns empty/garbled. Mandatory gate BEFORE every researcher+reviewer fan-out for LARGE/MASSIVE tasks. Closes the chunk decision at orchestrator level.
---

# Core Rule
Chunking bukan opsional - ini GATE sebelum fan-out. Kalau sub-agent dikasih task kegedean, outputnya kosong/garbled/mislabel. Orchestrator WAJIB jalanin Pre-Chunk Check dan dispatch per hasilnya.

# Pre-Chunk Checklist (HARD thresholds - jalanin SEBELUM fan-out)
Hitung untuk task yang mau di-dispatch:
- Q = jumlah pertanyaan/goal berbeda
- F = jumlah file berbeda yang disentuh
- O = jumlah format output diminta (code vs doc vs table vs web)

TRIGGER CHUNK jika SALAH SATU: Q >= 3 ATAU F >= 3 ATAU O >= 2.
- TRIVIAL/SMALL (Q<=2, F<=2, O=1): 1 chunk, fan-out normal (researcher || reviewer parallel).
- LARGE (trigger): pecah jadi 2-3 chunk.
- MASSIVE: pecah jadi 3-4 chunk.

# Chunk Sizing
Tiap chunk HARUS: <= 2 file, 1 fokus pertanyaan, 1 format output. Jangan gabungin 2 concern beda dalam 1 chunk.

# Dispatch Pattern (resolves sequential/parallel confusion)
- DALAM 1 chunk: researcher + reviewer di-dispatch PARALLEL (seperti biasa).
- ANTAR chunk: SEQUENTIAL. Chunk k+1 di-dispatch SETELAH chunk k selesai, membawa CONTEXT_SUMMARY (ringkasan hasil chunk k) agar agent berikutnya punya konteks tanpa baca ulang semua.
- Jangan dispat 1 task raksasa ke 1 agent. Jangan dispat semua chunk sekaligus tanpa urutan.

# Recovery (empty/garbled output)
- Kalau sub-agent balik KOSONG / garbled / mislabel: itu sinyal task masih kegedean ATAU model bermasalah.
- Jika model mati (ping guard skip): lanjut chunk lain / eskalasi ke Boss.
- Jika output kosong tapi model hidup: RE-CHUNK unit tsb jadi lebih kecil (pecah 1 file jadi per-fungsi, atau 1 pertanyaan jadi sub-pertanyaan). MAKSIMAL 2x re-chunk, lalu eskalasi ke Boss.
- Sub-agent boleh return `[CHUNK_REQUIRED]` kalau task tetap kegedean - orchestrator respons dengan re-chunk, BUKAN anggap gagal.

# Output
Orchestrator menghasilkan: (1) keputusan chunk (jumlah + isi tiap chunk), (2) urutan sequential, (3) CONTEXT_SUMMARY antar chunk. Ini masuk ke brief tiap agent.
