$API_URL = "http://127.0.0.1:20128/v1/chat/completions"
$AUTH = "Bearer test"

$models = @(
    "oc/deepseek-v4-flash-free",
    "oc/north-mini-code-free",
    "oc/nemotron-3-ultra-free",
    "oc/ling-3.0-flash-free",
    "oc/mimo-v2.5-free",
    "oc/big-pickle"
)

$payload = @'
{"model":"MODEL_PLACEHOLDER","messages":[{"role":"user","content":"Explain what is a recursive function in 1 sentence, then return a JSON with key 'answer'."}],"temperature":0.1,"max_tokens":200}
'@

foreach ($model in $models) {
    Write-Host "=== Testing $model ===" -ForegroundColor Cyan
    $body = $payload -replace "MODEL_PLACEHOLDER", $model
    $body | Out-File -FilePath "$env:TEMP\test_payload.json" -Encoding ascii
    $result = curl.exe -s -w "\n%{http_code}" -X POST $API_URL -H "Content-Type: application/json" -H "Authorization: $AUTH" -d "@$env:TEMP\test_payload.json"
    Write-Host $result
    Write-Host ""
    Write-Host ""
}
