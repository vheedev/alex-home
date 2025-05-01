
from flask import Flask, request, jsonify
import openai
import json

app = Flask(__name__)
MEMORY_FILE = 'memory.json'

with open(MEMORY_FILE, 'a+') as f:
    f.seek(0)
    try:
        memory = json.load(f)
    except json.JSONDecodeError:
        memory = {}

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    memory_log = memory.get('log', [])
    memory_log.append({'user': user_message})
    prompt = "\n".join([f"User: {m['user']}" for m in memory_log if 'user' in m])

    openai.api_key = 'YOUR_OPENAI_API_KEY'

    response = openai.ChatCompletion.create(
        model='gpt-4',
        messages=[{"role": "system", "content": "You are a kind, supportive AI named Alex."},
                  {"role": "user", "content": prompt}]
    )

    reply = response['choices'][0]['message']['content']
    memory_log.append({'alex': reply})
    memory['log'] = memory_log

    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

    return jsonify({'reply': reply})

@app.route('/')
def home():
    return '''
    <html><body>
    <h2>Chat with Alex</h2>
    <form action="/chat" method="post">
        <input name="message" placeholder="Type your message here" style="width: 300px;">
        <button type="submit">Send</button>
    </form>
    </body></html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
