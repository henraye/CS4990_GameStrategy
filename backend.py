from flask import Flask, request, jsonify, render_template
from openai import OpenAI

api_key = "redacted"
client = OpenAI(api_key=api_key)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def generate_game_strategy(game_description):
    game_description_prompt = (
        "I will be providing a description of a video game and a request. \n"
        "Please act as an esports coach for the game provided and come up with a strategy for the user's request in regards to the game they are playing and provide steps to achieve the strategy.\n"
        "I am going to provide a template for your output. CAPITALIZED WORDS are placeholders for content. This is the template below: \n"
        "<GAME NAME>: <STRATEGY> \n"
        "<NUMBERED STEPS>"
        "'<CHECKLIST>'\n"
        "----------------------- \n"
        + game_description
    )
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": game_description}
        ]
    )
    return completion.choices[0].message.content

def improve_game_strategy(game_description):
    game_description_prompt = (
        "I will be providing a description/checklist of a game strategy that ChatGPT has previously generated. \n"
        "Please act as an esports coach and improve the provided strategy by being more specific on terms that beginners may be unfamiliar with.  \n"
        "I am going to provide a template for your output. CAPITALIZED WORDS are placeholders for content. This is the template below: \n"
        "<GAME NAME>: <STRATEGY> \n"
        "<NUMBERED STEPS>"
        "'<CHECKLIST>'\n"
        "----------------------- \n"
        + game_description
    )
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": game_description}
        ]
    )
    return completion.choices[0].message.content

@app.route('/generate-strategy', methods=['POST'])
def generate_strategy():
    data = request.get_json()
    game_description = data.get('game_description')
    if not game_description:
        return jsonify({"error": "Game description is required"}), 400
    
    strategy = generate_game_strategy(game_description)
    strategy = strategy.replace('*', '').replace('#', '')
    return jsonify({"strategy": strategy})

@app.route('/improve-strategy', methods=['POST'])
def improve_strategy():
    data = request.get_json()
    game_description = data.get('game_description')
    if not game_description:
        return jsonify({"error": "Game description is required"}), 400
    
    strategy = improve_game_strategy(game_description)
    strategy = strategy.replace('*', '').replace('#', '')
    return jsonify({"strategy": strategy})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)