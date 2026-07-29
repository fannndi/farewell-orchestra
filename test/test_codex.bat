@echo off
setlocal enabledelayedexpansion

set API_URL=http://127.0.0.1:20128/v1/chat/completions

echo === Testing cx/gpt-5.6-luna — Basic ===
curl -s -w "\nHTTP %%{http_code}" -X POST "%API_URL%" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer test" ^
  -d "{\"model\":\"cx/gpt-5.6-luna\",\"messages\":[{\"role\":\"user\",\"content\":\"Explain what is a recursive function in 1 sentence, then return a JSON with key 'answer'.\"}],\"temperature\":0.1,\"max_tokens\":300}"

echo.
echo.

echo === Testing cx/gpt-5.6-luna — Tool Call ===
curl -s -w "\nHTTP %%{http_code}" -X POST "%API_URL%" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer test" ^
  -d "{\"model\":\"cx/gpt-5.6-luna\",\"messages\":[{\"role\":\"user\",\"content\":\"What is 25 + 17? Use a calculator.\"}],\"temperature\":0.1,\"max_tokens\":300,\"tools\":[{\"type\":\"function\",\"function\":{\"name\":\"calculator\",\"description\":\"Calculate expression\",\"parameters\":{\"type\":\"object\",\"properties\":{\"expression\":{\"type\":\"string\"}},\"required\":[\"expression\"]}}}]}"

echo.
echo.

echo === Testing cx/gpt-5.6-luna — Reasoning ===
curl -s -w "\nHTTP %%{http_code}" -X POST "%API_URL%" ^
  -H "Content-Type: application/json" ^
  -H "Authorization: Bearer test" ^
  -d "{\"model\":\"cx/gpt-5.6-luna\",\"messages\":[{\"role\":\"user\",\"content\":\"Write a Python function to find the longest palindrome substring. Return ONLY the code in a JSON with key 'code'.\"}],\"temperature\":0.1,\"max_tokens\":500}"

echo.
echo.

echo === CODEX TESTS DONE ===
