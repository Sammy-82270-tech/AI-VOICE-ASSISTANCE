import requests

def aiProcess(command):
    GEMINI_API_KEY = "AIzaSyBUobEQrRFPXvhK0pCKV8ROEGq7fn93vHY"   # <-- Replace with your Gemini API Key
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": command}
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        res_json = response.json()
        try:
            return res_json["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "Sorry, I could not parse Gemini's response."
    else:
        return f"Error {response.status_code}: {response.text}"
