from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

def perguntar(modelo, mensagem):
    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}"
        },
        json={
            "model": modelo,
            "messages": [
                {"role": "system", "content": "Você é NOVA, assistente inteligente."},
                {"role": "user", "content": mensagem}
            ]
        }
    )
    return r.json()["choices"][0]["message"]["content"]

@app.route("/nova", methods=["POST"])
def nova():
    msg = request.json["message"]

    r1 = perguntar("mistralai/mistral-7b-instruct", msg)
    r2 = perguntar("openchat/openchat-7b", f"Melhore: {r1}")

    return jsonify({"resposta": r2})
