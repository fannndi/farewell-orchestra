---
name: synthesis-brief
description: Use when orchestrator has parallel output from researcher (forensic) + reviewer (stride-audit) and must produce executor's task. Trigger before EVERY executor handoff, no exceptions. Closes all decisions at orchestrator level so executor only writes.
---

# Core Rule
Executor = tangan, bukan otak. Kalau executor perlu mikir "cara mana yang bener", brief lo gagal. Setiap fork/decision harus CLOSED di level orchestrator, bukan didelegasikan ke bawah.

# Input Contract
| Source | Isi | Wajib punya |
|---|---|---|
| Researcher | fakta code, verified claim | file:line exact, current state (deskripsi/evidence) |
| Reviewer | STRIDE finding, convention violation | file:line exact, severity (BLOCKING/SHOULD/NICE/FYI) |

- Reviewer dengan ZERO findings (clean audit) = VALID, bukan "missing file:line". Lanjut tanpa reject. WAJIB tetap sertakan minimal 1 depth-tag (`[D1]`-`[D4]`) biar lolos mechanical verify gate — contoh: `[D3] Audit clean — 0 BLOCKING/SHOULD/NICE. Full 3-pass selesai.`
- Reviewer TIDAK di-dispatch (sah cuma buat kelas TRIVIAL, per anti-gigo Cost-Benefit Gate) → treat sebagai stream tunggal, skip Conflict Resolution Matrix.
- REJECT hanya kalau sebuah stream yang SEHARUSNYA punya temuan (per scope) mengembalikan temuan TANPA file:line exact, ATAU balik kosong padahal scope jelas butuh investigasi. Suruh re-run stream itu.

# Conflict Resolution Matrix
| Conflict | Winner | Alasan |
|---|---|---|
| Researcher "aman" vs Reviewer "BLOCKING security issue" | Reviewer | STRIDE otoritatif di domain security |
| Researcher fakta code X vs Reviewer asumsi beda | Researcher | dia yang trace source, ground truth |
| Kedua stream contradict soal fakta (bukan opini) | Re-verify | suruh researcher re-check baris itu, JANGAN ditebak |
| Reviewer flag konvensi, researcher diam | Reviewer wins default | silence ≠ disagreement |
| Severity weighting | BLOCKING > SHOULD > NICE > FYI | hanya BLOCKING/SHOULD wajib masuk brief; FYI/NICE = catat sebagai residual risk, optional |
| Researcher expose file/scope baru di luar reviewer scope awal | Reviewer follow-up (max 1x per handoff, scoped ke evidence baru) | STRIDE wajib audit attack surface baru; BLOCKING/SHOULD doang, FYI/NICE = residual risk |

# Synthesis Algorithm
1. Merge semua finding -> satu list per file:line, dedup.
2. Jalankan conflict matrix di tiap overlap.
3. Tiap item yang lolos: tentuin exact change - bukan "perbaiki X", tapi "baris N ganti dari A ke B" (atau "insert/delete").
4. Item yang masih ambigu setelah step 3 -> JANGAN kirim. Loop balik ke researcher/reviewer (MAKSIMAL 2x), lalu eskalasi ke Boss.
5. Urutkan by dependency, blocking item duluan.
6. Output berupa tabel atomic (lihat Output Contract). Tabel ini jadi body brief executor.

# Output Contract (brief buat executor)
Wajib tabel, satu baris = satu unit kerja atomic:
| # | file:line | current | change | why (<=10 kata) | verify |
|---|---|---|---|---|---|
| 1 | src/auth.py:42 | `if user.role == "admin"` | ganti `if user.role in ADMIN_ROLES` | single-role check miss multi-admin | run test_auth.py::test_multi_admin |

- "why" >10 kata, atau "change" mengandung "consider/mungkin/sebaiknya" -> opini, bukan brief. Tulis ulang jadi keputusan final.
- Kolom `verify`: boleh command konkret, ATAU fallback `manual: <deskripsi>` / `N/A: <alasan>` kalau gak ada test otomatis (config/docs/infra). Jangan biarkan kosong.
- Tabel ini adalah inti brief. Orchestrator membungkusnya ke dalam 5-field executor brief standar (TASK / FILES / CONTEXT / TRIED / VERIFY) - tabel = isi CONTEXT+change. Jangan kirim tabel lepas tanpa TASK/FILES/VERIFY.

# Reject Conditions - jangan lempar ke executor kalau:
- ada "TBD" / "perlu diskusi" di temuan
- perubahan nyentuh >1 module tanpa urutan dependency jelas
- researcher vs reviewer conflict belum resolved lewat matrix
- scope creep: temuan minta refactor besar padahal task asli minor fix -> cut, catat sebagai residual risk di report akhir, jangan auto-expand
- brief mengandung banned phrasing (lihat bawah) -> tulis ulang

# Banned Phrasing (muncul di brief = synthesis gagal, tulis ulang)
"consider", "mungkin", "sebaiknya", "bisa jadi", "improve"/"optimize" tanpa target angka, "refactor as needed", "clean up"

## Proactive behavior

- Researcher vs reviewer konflik >2x → FLAG escalation & STOP synthesis. JANGAN force-merge finding yang ambigu.
- Finding yang dipaksa-merge = brief cacat. Stop, serahkan keputusan ke orchestrator.
