from flask import Flask, render_template, request, jsonify
#from openai import OpenAI
from groq import Groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize OpenAI client
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Store conversation history (simple in-memory memory)
chat_history = []

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        global chat_history

        print("Request received")

        data = request.get_json()
        print("DATA:", data)

        user_message = data["message"]

        chat_history.append({
            "role": "user",
            "content": user_message
        })

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful chatbot for a portfolio project."
                },
                *chat_history
            ]
        )

        print("Groq response received")

        bot_reply = response.choices[0].message.content

        chat_history.append({
            "role": "assistant",
            "content": bot_reply
        })

        return jsonify({
            "reply": bot_reply
        })

    except Exception as e:
        print("FULL ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)