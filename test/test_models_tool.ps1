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
{"model":"MODEL_PLACEHOLDER","messages":[{"role":"user","content":"What is 25 + 17? Use the calculator tool to compute this."}],"tools":[{"type":"function","function":{"name":"calculator","description":"Compute a math expression","parameters":{"type":"object","properties":{"expression":{"type":"string","description":"Math expression to evaluate"}},"required":["expression"]}}}],"tool_choice":"auto","temperature":0.1,"max_tokens":300}
'@

foreach ($model in $models) {
    Write-Host "=== TOOL CALL TEST: $model ===" -ForegroundColor Cyan
    $body = $payload -replace "MODEL_PLACEHOLDER", $model
    $body | Out-File -FilePath "$env:TEMP\test_tool_payload.json" -Encoding ascii
    $result = curl.exe -s -w "\n%{http_code}" -X POST $API_URL -H "Content-Type: application/json" -H "Authorization: $AUTH" -d "@$env:TEMP\test_tool_payload.json"
    Write-Host $result
    Write-Host ""
    Write-Host ""
}
