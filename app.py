
import os
from flask import Flask, request, render_template_string
import openai

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Chat with Alex</title>
</head>
<body>
    <h2>Chat with Alex</h2>
    <div id="chat-box">{{response|safe}}</div>
    <form method="post">
        <input type="text" name="message" placeholder="Type your message here" style="width: 300px;" />
        <button type="submit">Send</button>
    </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def chat():
    response_text = ""
    if request.method == "POST":
        user_message = request.form["message"]
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": user_message}]
            )
            response_text = f"<b>You:</b> {user_message}<br><b>Alex:</b> {completion.choices[0].message['content']}"
        except Exception as e:
            response_text = f"<b>You:</b> {user_message}<br><b>Alex (Error):</b> {str(e)}"
    return render_template_string(html, response=response_text)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
