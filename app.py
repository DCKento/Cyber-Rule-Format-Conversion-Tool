import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    user_input = request.form['user_input']
    selected_format = request.form['selected_format']

    # Set up the headers for the API request
    headers = {
        'Authorization': f'Bearer API_KEY_HERE',
        'Content-Type': 'application/json',
    }

    # Set up the data for the API request
    data = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": f"[Cybersecurity Rule Conversion] Please convert the following rule to {selected_format} format. If any part of the rule is unclear or the conversion isn't straightforward, please provide alternative suggestions along with explanations: {user_input}"
            }
        ]
    }

    # Make the API request
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data
    )

    # Handle the response
    response_data = response.json()
    if response.status_code == 200:
        # Assuming the converted rule is returned in this structure
        # Adjust according to the actual API response structure
        converted_rule = response_data['choices'][0]['message']['content']
    else:
        # Handle errors returned by the API
        converted_rule = f"Error: {response_data['error']['message']}"

    return jsonify({'converted_rule': converted_rule})

if __name__ == '__main__':
    app.run(debug=True)
