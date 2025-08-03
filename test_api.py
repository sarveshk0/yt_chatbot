import requests

url = "http://127.0.0.1:5000/ask"
payload = {
    "video_url": "https://www.youtube.com/watch?v=4ufdUg5TEVw",
    "question": "What is this video about?"
}

response = requests.post(url, json=payload)
print("Status Code:", response.status_code)
print("Response:", response.json())
