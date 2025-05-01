
from flask import Flask, request, jsonify, render_template_string
import openai
import json
import os

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

    openai.api_key = os.gatenv("OPENAI_API_KEY")

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": "You are a kind, supportive AI named Alex."},
                {"role": "user", "content": prompt}
            ]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"(Error: {str(e)})"

    memory_log.append({'alex': reply})
    memory['log'] = memory_log

    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

    return jsonify({'reply': reply})

@app.route('/')
def home():
    return render_template_string('''
    <html>
    <head>
        <title>Chat with Alex</title>
        <script>
            async function sendMessage() {
                const input = document.getElementById("message");
                const message = input.value.trim();
                if (!message) return;

                const chatBox = document.getElementById("chat");
                chatBox.innerHTML += "<b>You:</b> " + message + "<br>";
                input.value = "";

                try {
                    const response = await fetch("/chat", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({message})
                    });
                    const data = await response.json();
                    chatBox.innerHTML += "<b>Alex:</b> " + data.reply + "<br><br>";
                    chatBox.scrollTop = chatBox.scrollHeight;
                } catch (err) {
                    chatBox.innerHTML += "<i>(Failed to connect: " + err + ")</i><br>";
                }
            }

            window.addEventListener("DOMContentLoaded", () => {
                document.getElementById("sendBtn").onclick = sendMessage;
            });
        </script>
    </head>
    <body>
        <h2>Chat with Alex</h2>
        <div id="chat" style="width: 500px; height: 300px; border: 1px solid #ccc; padding: 10px; overflow-y: scroll;"></div>
        <input id="message" placeholder="Type your message here" style="width: 400px;">
        <button id="sendBtn">Send</button>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
