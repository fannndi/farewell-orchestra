@echo off
setlocal enabledelayedexpansion

set API_URL=http://127.0.0.1:20128/v1/chat/completions

echo === Testing OR google/gemma-4 (retry) ===
curl -s -w "\n%%{http_code}" -X POST "%API_URL%" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer test" ^
  -d "{\"model\":\"openrouter/google/gemma-4-26b-a4b-it:free\",\"messages\":[{\"role\":\"user\",\"content\":\"Explain what is a recursive function in 1 sentence, then return a JSON with key 'answer'.\"}],\"temperature\":0.1,\"max_tokens\":300}"
