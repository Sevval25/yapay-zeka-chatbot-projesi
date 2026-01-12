import httpx

try:
    r = httpx.get("https://api.openai.com/v1/models")
    print(r.status_code, r.text)
except Exception as e:
    print(e)
