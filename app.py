
from flask import Flask, request, render_template_string
import openai

app = Flask(__name__)

# Load API key from environment
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load Alex V1.0 personality from file
with open("alex_personality_prompt.txt", "r", encoding="utf-8") as f:
    alex_personality = f.read()

# HTML template with message box
html_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chat with Alex</title>
</head>
<body>
    <h1>Chat with Alex</h1>
    <div style="width: 100%; height: 300px; overflow-y: scroll; border: 1px solid #ccc;" id="chatbox">{{chatlog|safe}}</div>
    <form method="post">
        <input name="message" style="width: 80%;" placeholder="Type your message here" autofocus>
        <input type="submit" value="Send">
    </form>
</body>
</html>
'''

chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history
    if request.method == "POST":
        user_message = request.form["message"]
        chat_history.append(f"<b>You:</b> {user_message}")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": alex_personality},
                    {"role": "user", "content": user_message}
                ]
            )
            reply = response.choices[0].message["content"]
        except Exception as e:
            reply = f"<i>(Error: {e})</i>"

        chat_history.append(f"<b>Alex:</b> {reply.replace('\n', '<br>')}")
    
    rendered_chat = "<br>".join(chat_history[-20:])
    return render_template_string(html_template, chatlog=rendered_chat)

if __name__ == "__main__":
    app.run(debug=True)
