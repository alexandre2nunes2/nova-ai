from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

def perguntar(mensagem):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
               "model": "openchat/openchat-7b",
                "messages": [
                    {"role": "system", "content": "Você é NOVA, uma assistente inteligente, rápida e direta."},
                    {"role": "user", "content": mensagem}
                ],
                "max_tokens": 200
            },
            timeout=20
        )

        data = response.json()

        if "choices" not in data:
            return f"Erro da IA: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Erro interno: {str(e)}"


@app.route("/nova", methods=["POST"])
def nova():
    try:
        msg = request.json.get("message", "")

        if not msg:
            return jsonify({"resposta": "Mensagem vazia."})

        resposta = perguntar(msg)

        return jsonify({"resposta": resposta})

    except Exception as e:
        return jsonify({"resposta": f"Erro geral: {str(e)}"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
