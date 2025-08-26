import requests

def check_text(text, language="en-US", server_url="http://localhost:8010/v2/check"):
    try:
        data = {"text": text, "language": language}
        response = requests.post(server_url, data=data, timeout=5)
        response.raise_for_status()  # Raise exception for bad status codes
        matches = response.json()["matches"]
        return [
            {
                "error": match["message"],
                "suggestion": match["replacements"][0]["value"] if match["replacements"] else None,
                "context": match["context"]["text"]
            }
            for match in matches
        ]
    except requests.RequestException as e:
        return {"error": f"Server error: {e}"}

# Test the function
text = "I writed a essay and it have many mistake."
errors = check_text(text)

# Check if errors is a list or a dictionary
if isinstance(errors, dict) and "error" in errors:
    print(f"Failed to check text: {errors['error']}")
elif not errors:
    print("No errors found in the text.")
else:
    for error in errors:
        print(f"Error: {error['error']}")
        print(f"Suggestion: {error['suggestion']}")
        print(f"Context: {error['context']}")
        print("---")
