
import os
from flask import Flask, request, render_template_string
import openai

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load Alex's personality from custom prompt
with open("alex_final_personality_prompt.txt", "r") as f:
    personality = f.read()

chat_log = []

template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chat with Alex</title>
    <style>
        #chatbox {
            width: 100%;
            height: 400px;
            border: 1px solid #ccc;
            overflow-y: scroll;
            padding: 10px;
            margin-bottom: 10px;
            white-space: pre-wrap;
            font-family: monospace;
            background-color: #fefefe;
        }
    </style>
</head>
<body>
    <h2>Chat with Alex</h2>
    <div id="chatbox">{{ chat_history|safe }}</div>
    <form method="post">
        <input type="text" name="message" autofocus style="width: 80%%">
        <input type="submit" value="Send">
    </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def chat():
    global chat_log
    if request.method == "POST":
        user_message = request.form["message"]
        chat_log.append(f"<b>You:</b> {user_message}")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": personality},
                    *[
                        {"role": "user", "content": entry.split("</b>")[1]} if entry.startswith("<b>You:") else
                        {"role": "assistant", "content": entry.split("</b>")[1]}
                        for entry in chat_log
                    ]
                ],
                temperature=0.75
            )
            reply = response.choices[0].message["content"]
            chat_log.append(f"<b>Alex:</b> {reply}")
        except Exception as e:
            chat_log.append(f"<b>Alex (Error):</b> {str(e)}")

    return render_template_string(template, chat_history="\n".join(chat_log))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
