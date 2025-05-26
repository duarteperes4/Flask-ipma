from flask import Flask, render_template, request, flash, redirect, url_for
from ipma import previsao_por_cidade, CIDADES

# Constante para erros flash
ERROR_CATEGORY = "erro"

app = Flask(__name__)
app.secret_key = "segredo-ipma"

# Carrega a lista de cidades
CIDADES = sorted(CIDADES.keys())

def handle_error(message):
    """
    Função para lidar com erros, mostra uma mensagem flash e redireciona para a rota principal (index)
    """
    flash(message, ERROR_CATEGORY)
    return redirect(url_for("index"))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/resultado", methods=["GET"])
def resultado():
    cidade = request.args.get("cidade")
    if not cidade:
        return handle_error("Por favor, insira o nome de uma cidade.")
    
    try:
        previsao = previsao_por_cidade(cidade)
        return render_template("resultado.html", cidade=cidade, dias=previsao)
    except ValueError:
        return handle_error("A cidade não foi encontrada 😕")
    except Exception:
        return handle_error("Não foi possivel contactar a API do IPMA 🥴")

if __name__ == "__main__":
    app.run(debug=True)