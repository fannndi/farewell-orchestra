@echo off
setlocal enabledelayedexpansion

set API_URL=http://127.0.0.1:20128/v1/chat/completions
set PROMPT=Explain what is a recursive function in 1 sentence, then return a JSON with key 'answer'.

echo === Farewell Orchestra — OpenRouter Model Stress Test ===
echo.
echo Testing OR free models via 9router gateway...
echo.

for %%m in (
  "openrouter/nvidia/nemotron-3-ultra-550b-a55b:free"
  "openrouter/cohere/north-mini-code:free"
  "openrouter/google/gemma-4-26b-a4b-it:free"
  "openrouter/openai/gpt-oss-20b:free"
) do (
  echo === Testing %%m ===
  curl -s -w "\nHTTP %%{http_code}" -X POST "%API_URL%" ^
    -H "Content-Type: application/json" ^
    -H "Authorization: Bearer test" ^
    -d "{\"model\":%%m,\"messages\":[{\"role\":\"user\",\"content\":\"%PROMPT%\"}],\"temperature\":0.1,\"max_tokens\":300}"
  echo.
  echo.
)

echo === ALL OR TESTS DONE ===
pause
