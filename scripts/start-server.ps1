<#
.SYNOPSIS
    Start/stop opencode server (127.0.0.1:4096) untuk remote attach.

.DESCRIPTION
    Start:  powershell -File scripts/start-server.ps1
    Stop:   powershell -File scripts/start-server.ps1 -Stop
    Attach: opencode run --attach http://127.0.0.1:4096 --format json "Reply with exactly: OK"

.NOTES
    Security: bind 127.0.0.1 saja. Password wajib - env OPENCODE_SERVER_PASSWORD.
    Kalau kosong, script generate random 32-char sekali pakai (tampil di console).
    Log stdout/stderr: %TEMP%\opencode\server.log (+ server.err.log - Start-Process
    butuh file terpisah untuk stderr).
    Stop = kill process yang listen di port 4096 (opencode serve).
#>
param(
    [switch]$Stop
)

$LogDir = Join-Path $env:TEMP "opencode"
$OutLog = Join-Path $LogDir "server.log"
$ErrLog = Join-Path $LogDir "server.err.log"

if ($Stop) {
    $conns = Get-NetTCPConnection -LocalPort 4096 -State Listen -ErrorAction SilentlyContinue
    if ($conns) {
        $pids = $conns.OwningProcess | Sort-Object -Unique
        foreach ($procId in $pids) { Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue }
        Write-Host "[STOP] Killed process listening on 127.0.0.1:4096 (PID: $($pids -join ', '))"
    } else {
        Write-Host "[STOP] No process listening on port 4096 - server already stopped."
    }
    exit 0
}

# Password wajib - generate 32-char random kalau belum ada
if (-not $env:OPENCODE_SERVER_PASSWORD) {
    $bytes = New-Object byte[] 32
    [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
    $env:OPENCODE_SERVER_PASSWORD = -join ($bytes | ForEach-Object { $_.ToString("x2") })
    Write-Host "[INFO] OPENCODE_SERVER_PASSWORD kosong - generate 32-char random:"
    Write-Host "  $env:OPENCODE_SERVER_PASSWORD"
    Write-Host "  Set permanen: [Environment]::SetEnvironmentVariable('OPENCODE_SERVER_PASSWORD','<value>','User')"
} else {
    Write-Host "[INFO] Pakai OPENCODE_SERVER_PASSWORD yang sudah ada."
}

# opencode = npm shim (opencode.ps1) - jalankan lewat powershell baru
$cmd = (Get-Command "opencode" -ErrorAction Stop).Source

New-Item -ItemType Directory -Path $LogDir -Force | Out-Null

Start-Process -FilePath "powershell" `
    -ArgumentList "-NoProfile", "-File", $cmd, "serve", "--port", "4096", "--hostname", "127.0.0.1" `
    -RedirectStandardOutput $OutLog -RedirectStandardError $ErrLog -WindowStyle Hidden

Write-Host "[START] opencode serve -> http://127.0.0.1:4096 (log: $OutLog)"
