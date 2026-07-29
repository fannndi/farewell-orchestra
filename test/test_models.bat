@echo off
setlocal enabledelayedexpansion

set API_URL=http://127.0.0.1:20128/v1/chat/completions
set PROMPT=Explain what is a recursive function in 1 sentence, then return a JSON with key 'answer'.

echo === Farewell Orchestra — Model Stress Test ===
echo.
echo Testing OC free models via 9router gateway...
echo.

for %%m in (
  "oc/deepseek-v4-flash-free"
  "oc/north-mini-code-free"
  "oc/nemotron-3-ultra-free"
  "oc/ling-3.0-flash-free"
  "oc/mimo-v2.5-free"
  "oc/big-pickle"
) do (
  echo === Testing %%m ===
  curl -s -w "\nHTTP %%{http_code}" -X POST "%API_URL%" ^
    -H "Content-Type: application/json" ^
    -H "Authorization: Bearer test" ^
    -d "{\"model\":%%m,\"messages\":[{\"role\":\"user\",\"content\":\"%PROMPT%\"}],\"temperature\":0.1,\"max_tokens\":300}"
  echo.
  echo.
)

echo === ALL OC TESTS DONE ===
pause
