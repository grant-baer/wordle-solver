import requests
import json

url = 'https://wordle-api.vercel.app/api/wordle'
myobj = {
    "guess": "class"
}

response = requests.post(url, json=myobj)

if response.status_code == 200:
    # Parse the JSON response
    data = json.loads(response.text)

    # You can now access the data as a dictionary
    was_correct = data['was_correct']
    character_info = data['character_info']

    # Iterate through character_info
    for info in character_info:
        char = info['char']
        in_word = info['scoring']['in_word']
        correct_idx = info['scoring']['correct_idx']

        print(f"Character: {char}, In Word: {in_word}, Correct Index: {correct_idx}")

else:
    print("Failed to make the API request. Status code:", response.status_code)