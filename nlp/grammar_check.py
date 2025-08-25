import requests

url = "https://api.languagetool.org/v2/check"
data = {
    "text": "This is a example sentence.",
    "language": "en-US"
}
response = requests.post(url, data=data)
result = response.json()

for match in result["matches"]:
    print(f"Error: {match['message']}")
    print(f"Suggested fix: {match['replacements'][0]['value']}")
    print(f"Context: {match['context']['text']}")
    print("---")