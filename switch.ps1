param(
    [ValidateSet("pro", "flash", "free", "custom")]
    [string]$Profile = "pro"
)

switch ($Profile) {
    "pro"    { $heavy = "ocg/deepseek-v4-pro";       $light = "ocg/deepseek-v4-flash";      Write-Host "[Pro] orchestrator=Pro  workers=Flash" }
    "flash"  { $heavy = "ocg/deepseek-v4-flash";     $light = "oc/deepseek-v4-flash-free";  Write-Host "[Flash] orchestrator=Flash  workers=Free" }
    "free"   { $heavy = "oc/deepseek-v4-flash-free"; $light = "oc/deepseek-v4-flash-free";  Write-Host "[Free] all Free max hemat" }
    "custom" { Write-Host "[Custom] edit .env manually lalu run opencode"; exit 0 }
}

@"
NINEROUTER_API_KEY=sk_9router
ORCHESTRA_HEAVY_MODEL=$heavy
ORCHESTRA_LIGHT_MODEL=$light
"@ | Out-File -FilePath ".env" -Encoding ascii

Write-Host ".env updated. Starting OpenCode..."
Write-Host ""
opencode
