from flask import Flask, render_template, jsonify

app = Flask(__name__)

CATEGORIAS = [
    {"id": 1, "nome": "Mercados"},
    {"id": 2, "nome": "Alimentação"},
    {"id": 3, "nome": "Saúde"},
    {"id": 4, "nome": "Beleza"},
    {"id": 5, "nome": "Automotivo"},
    {"id": 6, "nome": "Construção"},
    {"id": 7, "nome": "Agropecuária"},
    {"id": 8, "nome": "Educação"},
    {"id": 9, "nome": "Profissionais"},
]


@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/loja-software")
def loja_de_software():
    return render_template("includes/page-loja-software.html")


@app.route("/catalogosd")
def catalogosd():
    return render_template("includes/page-catalogosd.html", categorias=CATEGORIAS)


@app.route("/catalogosd/catalogo")
def lista_catalogo():
    return jsonify(CATEGORIAS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
