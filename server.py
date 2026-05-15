from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

def perguntar(modelo, mensagem):
    try:
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

        data = r.json()

        # 🔥 proteção contra erro
        if "choices" not in data:
            return f"Erro da API: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Erro interno: {str(e)}"


@app.route("/nova", methods=["POST"])
def nova():
    try:
        msg = request.json["message"]

        r1 = perguntar("mistralai/mistral-7b-instruct", msg)
        r2 = perguntar("openchat/openchat-7b", f"Melhore: {r1}")

        return jsonify({"resposta": r2})

    except Exception as e:
        return jsonify({"resposta": f"Erro geral: {str(e)}"})


app.run(host="0.0.0.0", port=5000)
